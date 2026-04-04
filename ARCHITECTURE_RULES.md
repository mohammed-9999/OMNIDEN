# Architecture and Design Rules for Omniden

This document defines the coding standards and design patterns to be used for the development of the Omniden FastAPI backend. The goal is to ensure a robust, scalable, and production-ready application (Unified Search & Real-time Results).

## 1. Strict Separation of Concerns (MVC Approach)
To avoid chaotic code where everything is mixed together, business logic must be strictly separated from route definitions (Endpoints).
* **Routes (src/routes/)**: Must not contain any complex logic. They simply receive the user's search request, call the appropriate controller, and return the response.
* **Controllers (src/controllers/)**: This is the "brain" of Omniden. All processing logic (search orchestration, formatting Gemini requests) resides here.
* **Models (src/models/)**: Groups input and output data validation (Pydantic schemas) and database schemas.

## 2. The Factory Pattern and Interfaces (Extensibility)
Although Omniden currently uses the Gemini API for product search and analysis, the code must never be strongly tied to a single provider. If tomorrow we wish to use Claude or OpenAI to get better real-time results, the change must be made without rewriting the application.
* **The Rule**: Create an abstract interface (e.g., `ProductSearchInterface`) defining the mandatory methods (e.g., `search_products(query)`).
* **The Implementation**: Create a `GeminiProvider` that respects this interface.
* **The Factory**: Use an `LLMFactory` class that reads the configuration and automatically returns the correct provider.

## 3. The DRY Principle with the Base Controller
To avoid repeating the same initializations in each controller (e.g., loading settings, initializing the database or the Gemini API), use inheritance.
* **The Rule**: Create a `BaseController` that all other controllers will inherit from (like `SearchOrchestrator` or `GeminiController`).
* **Functionality**: The `BaseController` automatically loads global configurations in its constructor (`__init__`). Child controllers only have to call `super().__init__()` to access them.

## 4. Strict Configuration Validation (Pydantic)
Environment variables (like `GEMINI_API_KEY`, database credentials) must never be read with a simple `os.getenv()` scattered throughout the code.
* **The Rule**: Use `pydantic-settings` to define a `Settings` class (in `src/helpers/config.py`).
* **Advantage**: Pydantic will automatically validate the data types when the application starts. If the Gemini key is missing, the application will crash cleanly with a clear error message before even receiving requests. The actual `.env` file is ignored by Git, only `.env.example` is versioned.

## 5. Zero Magic Strings (Use of Enumerations)
The use of hardcoded strings (e.g., `return {"status": "success"}`) is forbidden because it complicates maintenance and testing.
* **The Rule**: All responses, statuses, and error signals must be centralized in Enumerations (Enums) (e.g., `models/enums/response_signals.py`).
* **Example**: Use `ResponseSignal.SEARCH_SUCCESS` or `ResponseSignal.GEMINI_TIMEOUT`. If the message needs to be modified, it will only be changed in one place.

## 6. Asynchronous Tasks and Idempotency (Performance)
To offer smooth "Real-time Results" without blocking the interface (Simplified UI), heavy requests to Gemini or e-commerce platforms must not block the main FastAPI thread.
* **Queues (Celery)**: Complex searches must be delegated to background "Workers".
* **Task Idempotency**: This is critical for optimizing Gemini API costs. A task must be "idempotent". If a user clicks "Search for iPhone 15" twice, the system must not launch two expensive requests.
* **The Rule (Idempotency Manager)**: Before launching the Gemini search, generate a "Hash" (e.g., SHA-256) based on the user's query. Check the database to see if this hash is already "Pending" or if it already has cached results. If yes, return the existing results or wait; otherwise, execute the request.