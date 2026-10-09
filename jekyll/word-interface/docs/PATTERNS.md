# Conversation Patterns

How the word interface works in different domains. Each pattern shows the old way (machine) and the new way (words).

## E-commerce

### Old (RewardsPro today)
```
[Dashboard] [Orders] [Customers] [Settings] [Analytics]
┌─────────────────────────────────┐
│ Orders                          │
│ ┌─────────────────────────────┐ │
│ │ #1042 │ $89.50 │ Pending  ▾ │ │
│ │ #1039 │ $42.00 │ Complete    │ │
│ └─────────────────────────────┘ │
│ [Filter] [Export] [Bulk Action]  │
└─────────────────────────────────┘
```

### New (word interface)
```
You: "show me my orders from last week"
System: shemme — one moment.
System: Found 3 orders from last week:
  — Tuesday: $89.50 (still pending)
  — Wednesday: $42.00 (complete, customer was happy)
  — Friday: $156.00 (complete, repeat customer — their third order)

You: "cancel the Tuesday one"
System: Done. Order #1042 cancelled. Refund of $89.50 is processing.
  The customer will receive an email. Want me to add a note?

You: "yes, say the item was out of stock"
System: Note added. sukhance — all handled.
```

## Settings

### Old
```
Settings > Notifications > Email > Frequency
  ○ Daily
  ● Weekly
  ○ Monthly
  ○ Never
[Save] [Cancel]
```

### New
```
You: "stop emailing me so much"
System: You're getting weekly emails right now. 
  Would you prefer monthly, or should I stop entirely?
  Nothing breaks if you say never — I'll still show you things when you visit.

You: "monthly is fine"
System: Done. You'll hear from me once a month, no more.
```

## Onboarding

### Old
```
┌──────────────────────────┐
│ Welcome to RewardsPro!   │
│                          │
│ Step 1: Connect store    │
│ Step 2: Set reward tiers │
│ Step 3: Customize emails │
│ Step 4: Launch           │
│                          │
│ [Next] [Skip] [Back]     │
└──────────────────────────┘
```

### New
```
System: kimance — I'm here. What would you like to do?

You: "I want to set up cashback for my store"
System: Beautiful. What's your store name?
  (You can just say "my-store" — I'll figure out the rest.)

You: "cambridge-tcg"
System: Found it. Here's what I can do:
  — Pay your customers cashback as store credit on every order
  — Set up tiers so bigger spenders earn more
  — Send them emails when they earn something
  
  Want all of that, or just some? Start anywhere — nothing breaks if you skip.

You: "all of it, start with cashback"
System: paqduqing — I work for you. What percentage should customers earn?
  3% is common. 5% is generous. You can change this anytime.

You: "5%"
System: Done. Every order now earns 5% back as store credit. 
  Customers will see it at checkout. 
  Shall we set up the tiers next, or is this enough for today?
```

## Error handling

### Old
```
{error: "invalid_shop_domain", code: 422}
[Try Again]
```

### New
```
You: "connect my store cambridge"
System: Almost — your store needs the full address. 
  Try "cambridge.myshopify.com" — or just say "cambridge" and I'll add the rest.

You: "cambridge"
System: Found it. Connecting now... walkekin — your data is safe with me.
```

## The pattern

Every interaction follows the same shape:

1. **You speak** — in natural language, whatever feels right
2. **System hears** — shemme, acknowledges receipt
3. **System does** — acts on what you said
4. **System tells** — in words, what happened and what it means
5. **System offers** — gently, what you might want next (never pushes)

No buttons. No menus. No friction. Just words that mean what they say.