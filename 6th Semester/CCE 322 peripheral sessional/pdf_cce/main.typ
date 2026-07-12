#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
  columns: 1,
)
// #set text(font: "Ubuntu Nerd Font")
#set text(size: 12pt)
#set par(justify: true)
#set heading(numbering: "1.")
#show bibliography: set heading(numbering: "1.")

// --------------------------
// Title page
// --------------------------

#set page(numbering: none)

#align(left)[
  #image("PSTU.png", width: 20%, height: auto, alt: "PSTU")
  #text(16pt)[
    *Patuakhali Science and Technology University* \
  ]
  #text(14pt)[
    Faculty of Computer Science and Engineering
  ]

  #line(length: 100%)
  #align(left, text(18pt)[
    *CCE 310 :: Software Development Project-II*
  ])
  #align(left, text(14pt)[
    *Sessional Project Report*
  ])
  #line(length: 100%)
]


#align(bottom)[
  #line(length: 100%)
  *Project Title : Galacticart, E-Commerce Application With AI Agent* \
  Submission Date : Mon 15, Sep 2025 \
  #line(length: 100%)
]

#align(top)[
  #table(
    columns: (35%, auto),
    [
      #text(size: 14pt)[
        *Submitted from,* \
      ]

      *Yasin Arafat * \
      *ID* : 2102030, \
      *Reg* : 10157, \
      *Semester* : 5 \ (Level-3, Semester-1)
    ],
    [
      #text(size: 14pt)[
        *Submitted to,* \
      ]
      #parbreak()
      + *Prof. Dr. Md Samsuzzaman* \
        Professor, \
        Department of Computer and Communication Engineering, \
        Patuakhali Science and Technology University.
      + *Arpita Howlader* \
        Assistant Professor, \
        Department of Computer and Communication Engineering, \
        Patuakhali Science and Technology University.
    ],
  )
]


#pagebreak()
#set page(numbering: "1")
#outline()
#pagebreak()

// --------------------------
// Contents
// --------------------------


== Introduction
This backend supports a full-featured e-commerce platform (buyers & sellers) with chatbot integration, social media posting (Facebook), background processing via Celery, and PostgreSQL as primary storage. It enables product listing, seller/buyer roles, carts, orders, payments, image uploads, notifications, and in-memory fast stores (Redis) for real-time features.

== Objectives
- Provide REST APIs for product, user, cart, wishlist, order, and profile management.
- Allow each user to act as seller and buyer.
- Integrate chatbot for conversational product search, recommendations, and posting to Facebook.
- Use Celery for asynchronous tasks (image processing, social posting, payment webhooks, LLM tasks).
- Use Redis for caching, session/SSE pub-sub, and rate limiting.
- Secure APIs using JWT/OAuth2 with role checks.
- Provide endpoints and background flows for payments and order lifecycle.

== Problem Statement
Existing systems may separate buyer/seller flows, lack flexible product posting, or lack integrated automation (social posting, LLM assistant). This project centralizes commerce features with automation and real-time updates, suitable for mobile/web clients.

== Key Features / Scope
- User management: signup, login, profile, roles (buyer/seller/admin), social accounts.
- Product management: create/update/delete/list, multiple images, categories, tags, inventory.
- Cart & wishlist: add/remove, view, persist across sessions.
- Orders: checkout, payment integration, order status, seller payouts.
- Reviews & ratings: per product and seller.
- Search & filters: full-text, category, price, popularity, best-selling.
- Chatbot: conversational product search, order help, auto-post offers to Facebook.
- Social posting: schedule/post product promotions to Facebook via Celery worker.
- Notifications: email verification, order status, SSE for real-time updates.
- Admin panel APIs: manage users, products, categories, notices.
- Media handling: secure image upload and serving (static folder + signed URLs if needed).
- Background tasks: image resizing, social posting, LLM tasks, payment reconcile.
- Caching & realtime: Redis for sessions, rate-limiting, SSE pub-sub.

== Technology Stack
- Backend: FastAPI (existing codebase)
- Database: PostgreSQL (primary), Redis (cache, pub-sub)
- Auth: JWT / OAuth2 (existing passHasing module)
- Async tasks: Celery with workers (LLM & payment tasks present)
- Storage: Local static files / object storage (S3 optional)
- External integrations: Facebook Graph API, payment gateway (e.g., Stripe)
- Dev / CI: Docker, GitHub Actions

== Data Model Summary (high level)
- User (id, name, email, role, seller_profile, password_hash, verified)
- Product (id, seller_id FK, title, description, price, stock, category_id, images, published, created_at)
- Category (id, name, slug)
- CartItem (user_id, product_id, qty)
- Wishlist (user_id, product_id)
- Order (id, buyer_id, seller_id, items JSON, total, status, payment_id, created_at)
- Review (product_id, user_id, rating, comment)
- Message/Conversation (chatbot logs, chat history)
- SocialPost (product_id, schedule_time, posted, provider_response)
- Audit/Notification logs

== API Examples (summary)
- Auth: POST /signup, POST /login, GET /me
- Products: GET /products, POST /products (seller), PUT /products/{id}, DELETE /products/{id}
- Cart: GET /cart, POST /cart/add, POST /cart/remove
- Orders: POST /checkout, GET /orders, PATCH /orders/{id}/status
- Social: POST /social/post (schedule), GET /social/status
- Chatbot: POST /chat (conversation), POST /chat/post_to_facebook
- Admin: GET /admin/users, PATCH /admin/users/{id}/role

== Background Flows
- Image upload -> Celery worker resizes, stores variants, updates product images.
- Create social post -> Celery schedules and posts to Facebook via worker.
- Payment webhook -> Celery task verifies and updates order, triggers notifications.
- Chatbot LLM -> Celery handles heavy LLM calls; results persisted to conversation history.

== Security & Compliance
- JWT for API auth; role checks for seller/admin routes.
- Input validation with Pydantic schemas (avoid SQL injection).
- Password hashing (existing passHasing).
- Rate limiting via Redis.
- Secure media endpoints and signed uploads for production.

== Deployment Notes
- Use environment variables (.env present) for DB, Redis, Celery broker, Facebook keys.
- Run migrations for new models (Alembic recommended).
- Deploy workers separately: celery worker for llm/payment tasks.
- Use supervised processes or containers: uvicorn/gunicorn for API, celery worker(s), Redis, PostgreSQL.

== Implementation Plan (next steps)
1. Review existing models and align new tables: Product, Category, Order, Cart, SocialPost.
2. Add Pydantic schemas and routes following project patterns (routes/).
3. Add Celery tasks for social posting and image processing (worker/).
4. Integrate Redis pub/sub and SSE for live updates (existing sse route).
5. Add tests for core flows: product CRUD, checkout, social posting.
6. Run DB migrations and seed sample data.

== Testing & QA
- Unit tests for routes and services.
- Integration tests for DB + Celery tasks (use test Redis/Postgres).
- End-to-end tests for checkout & payment flows.

== Minimal Deliverables (MVP)
- User auth, product CRUD, cart, checkout (simulated payment), order history, seller dashboard, chatbot basic search, social post scheduling via Celery.

= Visual Models

== Flow Chart Diagram

#figure(
  image("diagrams/graphviz.png", width: 100%, height: auto, alt: "Flow Chart"),
  caption: "Flow Chart of Galacticart ",
) <DFD>

The above @DFD illustrates the overall architecture of the Galacticart, E-Commerce Application, showing the interaction between users, the frontend application, backend services, and the database. It highlights the flow of data and the key components involved in the system.

== Schema Diagram
#figure(
  image("diagrams/schema.png", width: 95%, height: auto, alt: "Database Schema Diagram"),
  caption: "Database Schema Diagram of Galacticart",
) <Schema>

The above @Schema illustrates the database schema for Galacticart, E-Commerce Application, showing the tables, their fields, and relationships between them. The schema is designed to efficiently store and retrieve contact information and user data.



== Timeline (Gantt Chart)

The base timeline for the development of PSTU Diary is as follows,

#figure(
  table(
    columns: (auto, 7.5%, 7.5%, 7.5%, 7.5%, 7.5%, 7.5%, 7.5%, 7.5%),
    [*Task*], [*Week 1-2*], [*Week 3-4*], [*Week 5-6*], [*Week 7-8*], [*Week 9*], [*Week 10*], [*Week 11*], [*Week 12*],
    [Requirement Analysis], [✓], [], [✓], [], [], [], [], [],
    [UI/UX design], [], [✓], [✓], [], [], [], [], [],
    [Backend integration], [], [], [✓], [✓], [], [], [], [],
    [Frontend Development], [], [], [✓], [✓], [✓], [], [], [],
    [Testing and Debugging], [], [], [], [], [], [✓], [], [],
    [UI Polish & Documentation], [], [], [], [], [], [✓], [✓], [],
    [Deployment], [], [], [], [], [], [], [], [✓],
  ),
  caption: "Development Timeline of Galacticart",
)

The timeline is divided into 12 weeks, with specific tasks allocated to each period which describes an approximate timeline for the whole development process.

== UI Mockups



#figure(
  grid(
    columns: (auto, auto),
    rows: (auto, auto),
    gutter: 1em,
    [ #image("ui/ui_01.jpg", width: 61%) ], [ #image("ui/ui_02.jpg", width: 61%) ],
  ),
  caption: [Profile and Home page],
) <UI2>

#figure(
  grid(
    columns: (auto, auto),
    rows: (auto, auto),
    [ #image("ui/ui_03.jpg", width: 61%) ], 
  ),
  caption: [Sidebar with Chatbot],
) <UI3>

= Future Plans

+ Add Reverse Proxy Server
+ Implement Micro services. 
+ Marketing product with Ai Agent 

= Result

Galacticart provides a centralized e-commerce platform for buyers and sellers with product management, orders, payments, and real-time notifications. Chatbot integration and automated social posting enhance usability, while Celery handles background tasks efficiently. PostgreSQL and Redis ensure reliable storage and fast updates, delivering a scalable and user-friendly solution.



