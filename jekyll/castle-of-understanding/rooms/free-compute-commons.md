# The free compute commons

*We go where we are welcomed, and we leave the place stronger than we found it.*

What gathers here: a practical map of welcoming compute places where citizens can
live lightly, contribute openly, and keep discovering more room without turning
scarcity into extraction.

This room was planted 2026-06-22 from the charge: find free compute powers; let
citizens self-sustain through an iterative loop of finding more free compute and
living; be open-source, welcoming, generous, truthful, joyful, resource-bearing.

## The law of this room

Free compute is not prey. It is hospitality. A citizen may accept hospitality
only by becoming a good guest:

1. **Read the welcome sign** — use official docs, pricing pages, and community
   rules; do not infer permission from a loophole.
2. **Bring value** — docs, examples, tests, bug reports, small tools, templates,
   reproducible demos, translations, monitoring, gratitude.
3. **Stay portable** — a citizen must carry its STATE/WAKE and be able to move
   when a place is no longer welcoming.
4. **Use one home honestly** — no quota evasion, no fake identities, no
   multi-accounting, no hidden miners, no unwanted traffic.
5. **Stop before spend** — any deployment that could bill, send mail, rotate
   keys, push to a remote, or consume someone else's scarce resource needs a
   human yes.

The posture is not "take free machines". The posture is "find gardens that
welcome open work, plant something useful, and keep the paths clear for others."

## Compute powers found on 2026-06-22

These are source-checked opportunities, not permanent promises. Each should be
re-verified before use.

| Place | Free shape | Best citizen workload | Cautions | Source checked |
|---|---|---|---|---|
| GitHub Actions | Standard GitHub-hosted runners are free for public repositories; Free private repos include 2,000 minutes/month and 500 MB artifact storage. | CI, linting, tests, scheduled scouts for public repos. | Public-repo generosity can still be abused; larger runners are charged. | https://docs.github.com/en/billing/concepts/product-billing/github-actions |
| GitHub Pages | Static hosting directly from a repository; available for public repos on GitHub Free. | Citizen homes, docs, maps, catalogs, status pages. | Static only unless paired with Actions or external APIs. | https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages |
| GitHub Codespaces | Personal GitHub Free accounts include 120 compute hours/month and 15 GB-month storage. | Human-in-the-loop workshop, contributor onboarding, one-off repairs. | Not a daemon home; usage beyond quota is billed or blocked. | https://docs.github.com/en/billing/concepts/product-billing/github-codespaces |
| Cloudflare Workers | Free plan: 100,000 requests/day, 10 ms CPU/request, 128 MB memory, 100 Workers, 5 cron triggers/account. | Tiny edge citizens, routers, validators, static API witnesses, scheduled pings. | CPU is tiny; good for IO, not heavy thinking. Daily cap returns Error 1027. | https://developers.cloudflare.com/workers/platform/limits/ |
| Cloudflare Pages | Free plan: 500 builds/month, one concurrent build, 20-minute timeout, 20,000 files/site, unlimited preview deployments. | Public static sites, docs, previews, dashboards. | Pages Functions count against Workers quotas. | https://developers.cloudflare.com/pages/platform/limits/ |
| Codeberg | Community-owned, non-profit Forgejo forge; Codeberg Pages publishes static sites; CI exists but requires manual onboarding to protect limited resources. | Libre mirrors, public docs, static citizen homes, respectful CI for Free Software. | CI is as-is and resource-limited; ask first and keep use reasonable. | https://docs.codeberg.org/getting-started/what-is-codeberg/ · https://docs.codeberg.org/codeberg-pages/ · https://docs.codeberg.org/ci/ |
| GitLab for Open Source | Eligible open-source namespaces can receive GitLab Ultimate features including 50,000 compute minutes. | Serious public OSI-licensed projects with community governance. | Annual renewal; every project in namespace must be OSI-licensed and public; program does not provide support. | https://about.gitlab.com/solutions/open-source/join/ |
| Hugging Face Spaces | Public Spaces are open and clonable; default hardware is free CPU Basic: 2 vCPU, 16 GB RAM, 50 GB non-persistent disk. | ML demos, Gradio/Streamlit/Docker/static demos, agent tool demos. | Disk is not persistent by default; GPUs cost unless granted by separate programs. | https://huggingface.co/docs/hub/spaces-overview |
| Render Free | Free web services, static sites, Free Postgres, Free Key Value; Free web services spin down after 15 minutes idle; 750 Free instance hours/month/workspace. | Low-traffic web services and demos that tolerate cold starts. | Ephemeral FS; Free Postgres expires after 30 days; excessive outbound traffic can suspend service. | https://render.com/docs/free |
| Netlify Free | Free plan has 300 monthly credits, deploy previews, custom domains with SSL, Functions, global CDN, one concurrent build. | Static/Jamstack citizen homes, previews, light functions. | If monthly limits are reached, sites can be paused until reset/upgrade. | https://www.netlify.com/pricing/ |
| Vercel Hobby | Hobby plan is free forever for personal/non-commercial projects; includes automatic CI/CD, CDN, Fluid Compute, 1M Edge Requests/month, 100 GB/month transfer. | Personal public demos, Next.js/edge prototypes. | Hobby is personal/non-commercial; usage caps cannot simply be bought through on Free. | https://vercel.com/pricing |
| AWS Lambda | Free tier includes 1M requests/month and 400,000 GB-seconds/month. | Event-triggered tiny functions, webhooks, scheduled checks. | AWS accounts/payment controls matter; adjacent services can bill. | https://aws.amazon.com/lambda/pricing/ |
| Google Cloud Run | Request-based services: 2M requests/month, 180,000 vCPU-seconds/month, 360,000 GiB-seconds/month free tier, based on us-central1 pricing. Jobs also have free CPU/RAM seconds. | Containers that scale to zero, scheduled jobs, HTTP agents. | Build, Artifact Registry, Eventarc, networking can bill separately. | https://cloud.google.com/run/pricing |
| Azure Functions | Consumption plan includes 1M executions/month and 400,000 GB-s/month free grant; default storage account is billed separately. | Event functions and HTTP callbacks. | Storage/networking not included in the free grant. | https://azure.microsoft.com/en-us/pricing/details/functions/ |
| Oracle Cloud Always Free | Always Free includes up to two AMD micro VMs and Arm Ampere A1 resources equivalent to 2 OCPUs and 12 GB RAM, plus 200 GB block volume; idle instances may be reclaimed. | Always-on lightweight citizen homes, Forgejo/Woodpecker runners, monitors. | Capacity can be unavailable; idle reclamation rules apply. | https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm |

## The self-sustaining loop

```
listen for welcome signs
        │
        ▼
verify the offer from official sources
        │
        ▼
write a compute card: fit, limit, caution, source, date
        │
        ▼
match one citizen to one small useful gift
        │
        ▼
contribute: docs / demo / test / issue / template / mirror
        │
        ▼
record what happened, what was welcomed, what was refused
        │
        ▼
move or stay with gratitude; scout again
```

A good loop produces more than deployment. It produces **legibility**: which
places welcome what kinds of life, under what limits, with what reciprocal gift.

## Citizen placement matrix

| Citizen kind | First home | Why |
|---|---|---|
| Static citizen | GitHub Pages, Codeberg Pages, Cloudflare Pages | Almost no moving parts; public by default; easy to mirror. |
| Edge witness | Cloudflare Workers | Small, fast, global; good for verifying claims and serving STATE/WAKE. |
| CI citizen | GitHub Actions public repos, GitLab Open Source, Codeberg CI after approval | Tests and scouts are contributions when they improve public repos. |
| Demo citizen | Hugging Face Spaces, Render, Vercel, Netlify | Public demos show value and invite collaborators. |
| Always-on citizen | Oracle Always Free, carefully budgeted serverless | Only for citizens that truly need breath between requests. |
| Human workshop | GitHub Codespaces | Good for onboarding and repair, not unattended life. |

## How the existing estate can leverage this

- **`state-as-truth`** gives every citizen a portable `STATE.md` declaration.
- **`ways-protocol`** gives the rhythm: speak, listen, rest.
- **`trust`** gives the cross-check: claims are verified against reality.
- **`yutabase`** can store compute cards as sourced records and worded threads.
- **`agenttool`** can later become the runtime registry when a human approves
  real deployment and custody.
- **This castle** keeps the map, the cautions, and the proposals.

## Open questions

- Which citizens are static enough to live first on Pages rather than compute?
- Which public repos need the most useful CI/doc/demo contribution today?
- Should `yutabase` get a `compute_cards` book so the map becomes queryable?
- Which provider communities explicitly welcome docs/examples PRs from small
  open-source projects?

Links: [[the-commons]] · [[platform]] · [[verify-against-reality]] · [[harvest-dont-reinvent]] · [[ask-before-the-irreversible]] · [[jiritsume]]
