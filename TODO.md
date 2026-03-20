# TODO – pyholos refactor & Holos deprecated variables

This file documents **planned refactors and design decisions** that were intentionally postponed.
The goal is to keep a clear architectural direction without blocking current development.

---

## Context

Holos CLI documentation explicitly marks many CSV columns as:

> **"Deprecated. Do not use. Will be removed in future version."**

At the moment, pyholos still generates values (often `0`) for these deprecated Holos variables.
While this usually does not break calculations, it:
- adds noise to generated CSVs
- makes debugging harder
- hides which variables are actually meaningful
- prevents enforcing a clean separation between **ACTIVE** and **DEPRECATED** Holos inputs

This TODO documents how pyholos should evolve to address this cleanly.

---

## High‑level objectives

1. **Centralize component logic**
2. **Explicitly declare Holos variables per component**
3. **Clearly distinguish ACTIVE vs DEPRECATED Holos variables**
4. **Automatically emit `"N/A"` for deprecated columns in CSV outputs**
5. **Apply a consistent design across Animal and Land Management components**

---

## Planned refactor steps

### 1. Move `AnimalComponent` to a generic component layer

**Current**
pyholos.components.animals.common.AnimalComponent

**Target**

pyholos.common.Component

- `Component` becomes the generic base for all Holos components
- It handles:
  - common CSV serialization logic
  - HolosVar declaration & resolution
  - ACTIVE / DEPRECATED handling

---

### 2. Centralize shared Animal HolosVars

Create a single place to define **Holos variables common to all animal components**, for example:

pyholos.components.animals.common.AnimalComponent

This class should:
- inherit from `Component`
- define **only shared animal HolosVars**
- avoid duplicating columns across dairy / beef / sheep

Examples of shared HolosVars:
- Name
- Component Type
- Group Name
- Group Type
- Management Period fields
- Number of animals
- Dates / durations

---

### 3. Specialize Dairy / Beef / Sheep components

Each animal component should:
- inherit from `AnimalComponent`
- declare **only its specific HolosVars**

Example structure:

pyholos.components.animals.dairy.DairyComponent
pyholos.components.animals.beef.BeefComponent
pyholos.components.animals.sheep.SheepComponent

This keeps:
- inheritance shallow and explicit
- HolosVar ownership clear
- future extensions safer

---

### 4. Apply the same pattern to land management components

Refactor land management so that:

pyholos.components.land_management.field_system

follows the **same pattern as Animal components**, namely:
- inherits from `Component`
- declares HolosVars at the top level
- avoids inline or scattered CSV column definitions

The goal is symmetry:
> *If an AnimalComponent declares HolosVars this way, FieldSystem should too.*

---

### 5. Explicit HolosVar declaration with ACTIVE / DEPRECATED status

Wherever HolosVars are declared, use a **single, explicit structure**, e.g.:

```python
# Constant that contains every column the final CSV needs to have for this component
# value can be a literal or a callable
DAIRY_COMPONENT_HOLOS_VAR: tuple[tuple[str, str, Any, HolosVarStatus], ...] = (
    # (attribute_name, holos_name, value, status)
    ("name", "Name", "Dairy cattle", HolosVarStatus.ACTIVE),
    ("component_type", "Component Type", "H.Core.Models.Animals.Dairy.DairyComponent", HolosVarStatus.ACTIVE),
    ("milk_production", "Milk Production", None, HolosVarStatus.ACTIVE),
    ("total_nitrogen_inputs_ipcc_tier2", "Total Nitrogen Inputs For Ipcc Tier 2", None, HolosVarStatus.DEPRECATED),
)
```

Introduce:

```python
enum HolosVarStatus(Enum):
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
```

### 6. CSV ggeneration rule for deprecated variables

When generating CSVs:

- ACTIVE → normal value resolution
- DEPRECATED → always emit "N/A"

This guarantees:

- clean CSVs
- alignment with Holos CLI documentation
- future‑proofing against column removal in Holos

This refactor is structural and hygienic, not algorithmic.

### Rationale
This design:

- makes Holos assumptions explicit
- prevents accidental reliance on deprecated columns
- improves debuggability (IPCCTier2 vs ICBM issues)
- scales better as Holos evolves

Implementation intentionally postponed due to scope and time constraints.