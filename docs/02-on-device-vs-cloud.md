# Chapter 2. On-Device vs Cloud Models

*Where does your question actually go? Two very different answers — and when each one is the right choice.*

## The short version

There are two kinds of AI you can use on a phone:

- **Cloud AI** phones home. Your question travels over the internet to a large computer in a data center; the answer travels back. Nearly every big-name chat app works this way.
- **On-device (local) AI** never leaves your phone. A small model runs on the phone's own chip. No internet needed, no data used, nothing transmitted.

Both are real AI. They're just good at different things — like a home library versus a giant city library.

## What "model" means (in one paragraph)

A *model* is the trained brain of the AI — the part that actually writes the answers. Large models run on rows of rented computers in warehouses (that's "the cloud"). Small models are shrunk-down cousins tuned to run on phone chips. Same core idea, different muscle: cloud models know more, local models leak less.

## Head-to-head

| | Cloud AI | On-device AI |
|---|---|---|
| Internet needed | Yes | No |
| Smartness ceiling | Highest — the biggest models | Smaller — good, not genius |
| Works offline (basement, airplane, dead zone) | No | Yes |
| Uses your mobile data | Yes, per message | No |
| Battery | Light (mostly network) | Heavy *while* answering, zero when idle |
| Speed | Fast, up to your network speed | Slower on older phones, quick on new ones |
| Phone requirements | Nearly any smartphone | Needs a fairly recent phone |
| Privacy | Depends on the company's policy (see Chapter 4) | Strongest by default: nothing travels |
| Cost | Free tier or subscription | Usually nothing |

## The middle case: features built into your phone

You may already own on-device AI without installing anything. Recent iPhones and many current Android phones ship with built-in assistants that can summarize notifications, proofread text, and answer questions — partly on the phone itself, partly in a private cloud run by the phone maker. Check **Settings** and search for "AI" or your phone's assistant name. It's worth 10 minutes just to know what's there.

## When to use each one

**Use cloud AI when:**

- the question is hard and deserves the smartest model available,
- you're on Wi-Fi anyway,
- the task involves long documents or images (cloud models handle big files better).

**Prefer local (or no AI at all) when:**

- the topic is private: health details, financial numbers, legal trouble, angry drafts about a coworker,
- you're offline or out of data,
- you just need a quick rewrite or summary and don't want to wait on the internet.

## A realistic privacy middle ground

If going fully local isn't possible on your phone, you can still lower risk in two easy steps:

1. Keep private details out of prompts. Instead of pasting an entire medical bill, ask "how do I ask a billing office to explain a charge I don't recognize?" — the *pattern*, not the paperwork.
2. Turn off chat-history training in the app's settings (Chapter 4 shows where it usually hides).

## Going all-in on local AI (optional next step)

Some phones and a few free apps let you *deliberately* download a small model and chat fully offline. Chapter-level walkthroughs live in the companion book *The Massive AI Manual* ("Local AI" chapter). Two honest warnings first: local models are noticeably less capable than cloud ones, and downloading them takes real space (several gigabytes on modern phones). Free on Wi-Fi, though.

## The 10-second chooser

Ask two questions:

1. **Does this involve anything private?** → lean local, or strip the details out (Chapter 4).
2. **Am I offline or out of data?** → local wins instantly.

Otherwise, default to cloud for the smartest answer — free tiers are genuinely good now.

## Checkpoint

You should now be able to:

- Say in one sentence what a "model" is.
- Name three situations where local AI is the better call.
- Find out whether your phone already has a built-in assistant.

Next up: talking to AI instead of typing to it.

[Next: Chapter 3 — Voice Input](03-voice-input.md)
