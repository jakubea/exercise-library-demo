# Programmatic SEO – Exercise Library

A demonstration project exploring how programmatic SEO can be used to generate scalable, search-friendly landing pages from structured data.

**Live demo:** https://exercise-library-demo.jakubea.workers.dev/

## Project overview

The project demonstrates how a structured dataset and reusable page templates can be combined to automatically generate multiple types of SEO-friendly landing pages.

The exercise library uses exercise attributes such as muscle group, equipment and difficulty level to create pages targeting different search intents, rather than manually creating each page.

## Generated page types

The generator creates:

- **Homepage** – overview of the exercise library.
- **Muscle group pages** – exercises grouped by primary muscle group.
- **Exercise detail pages** – individual exercise descriptions, instructions and common mistakes.
- **Equipment pages** – exercises grouped by required equipment.
- **Difficulty pages** – exercises grouped by difficulty level.

## Data structure

The source dataset is stored in `exercises.csv`. Each row represents one exercise and contains the following attributes:

| Attribute | Description |
|---|---|
| `name` | Exercise name |
| `muscle` | Primary muscle group |
| `secondary` | Secondary muscle groups |
| `equipment` | Required equipment |
| `level` | Difficulty level |
| `type` | Exercise type |
| `steps` | Exercise instructions |
| `mistakes` | Common mistakes |
| `video` | Video reference |

The attributes are used to group exercises, determine page relationships and generate relevant landing pages.

## SEO implementation

The project demonstrates several programmatic SEO concepts:

- Structured data as the source of page content.
- Reusable templates for consistent page generation.
- Descriptive and hierarchical URL structures.
- Dynamically generated page titles and meta descriptions.
- Canonical URLs.
- Breadcrumb navigation and structured data (`BreadcrumbList`, `HowTo`).
- Internal linking between related pages.
- XML sitemap generation.
- `robots.txt` configuration.
- Minimum record thresholds for equipment and difficulty pages to help prevent thin content.

## How it works

A Python script (`build.py`) processes the CSV dataset and generates a static website.

To rebuild the website locally:

```bash
python3 build.py
```

The generated files are written to the `dist/` directory, including HTML pages, `sitemap.xml` and `robots.txt`.

## Tools and technologies

- Python – static site generation
- CSV – structured source data
- HTML – generated pages
- XML – sitemap

## Project approach

I designed the data structure, page types, URL logic and SEO requirements. I used AI assistance to implement the generator and supporting code, while focusing on the underlying programmatic SEO architecture and understanding how the different components work together.

The project is intended to demonstrate the SEO strategy, data modelling and page-generation logic behind a scalable pSEO website, rather than serve as a production-ready application.

---

*This is a learning and demonstration project. The dataset is illustrative and is not intended to represent a complete or authoritative exercise database.*
