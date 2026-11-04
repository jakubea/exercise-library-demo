# Programmatic SEO – Exercise Library

A small demonstration project exploring how programmatic SEO can be used to generate structured landing pages from a dataset.

**Live demo:** https://exercise-library-demo.jakubea.workers.dev/

## Project overview

The goal was to build an exercise library that automatically generates SEO-friendly pages based on structured exercise data.

Instead of creating each page manually, the project uses a dataset and reusable HTML templates to generate multiple types of landing pages targeting different search intents.

## Page types

The generator creates:

- **Homepage** – overview of the exercise library.
- **Muscle group pages** – exercises grouped by primary muscle group.
- **Exercise detail pages** – individual pages with exercise descriptions, instructions and common mistakes.
- **Equipment pages** – exercises grouped by equipment.
- **Difficulty pages** – exercises grouped by difficulty level.

## Data structure

The source dataset is stored in `exercises.csv`.

Each row represents one exercise and contains the following attributes:

| Attribute | Description |
|---|---|
| `name` | Exercise name |
| `muscle` | Primary muscle group |
| `secondary` | Secondary muscle groups |
| `equipment` | Required equipment |
| `level` | Difficulty level |
| `type` | Exercise type |
| `steps` | Instructions |
| `mistakes` | Common mistakes |
| `video` | Video reference |

These attributes determine how exercises are grouped and which landing pages are generated.

## SEO implementation

The project demonstrates several core programmatic SEO principles:

- Structured data as the source of content.
- Reusable page templates.
- Consistent and descriptive URL structures.
- Unique page titles and meta descriptions.
- Canonical URLs.
- Breadcrumb navigation and structured data (`BreadcrumbList`, `HowTo`).
- Internal linking between related pages.
- XML sitemap generation.
- `robots.txt` configuration.
- Minimum record thresholds for generating equipment and difficulty pages to reduce thin content.

## How it works

The project uses a Python script (`build.py`) to process the CSV dataset and generate static HTML pages.

To rebuild the website:

```bash
python3 build.py
```

The generated website is written to the `dist/` directory, including HTML pages, `sitemap.xml` and `robots.txt`.

## Tools and technologies

- Python – static page generation
- CSV – structured source data
- HTML – page templates and generated pages
- XML – sitemap

## Project approach

I defined the dataset structure, page types, URL logic and SEO requirements. The implementation was developed with AI assistance, which I used to help build the generator and its supporting code.

The main focus was understanding how structured data, templates and SEO rules work together to create scalable landing pages, rather than building a production-ready software application.

---

*This is a learning and demonstration project. The dataset is illustrative and is not intended to represent a complete or authoritative exercise database.*
