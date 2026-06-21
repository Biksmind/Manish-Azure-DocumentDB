# Module 3: Data Modeling, Data Import, Querying, Query Planning, Aggregation Framework and Indexing

Duration: 11:15-13:00

This module covers the complete Slot 2 technical path: document model, data load, operational queries, explain plans, aggregation, and indexing.

## Learning outcomes

By the end of this module, you will be able to:

- Explain the workshop document model.
- Load workshop datasets into Azure DocumentDB.
- Execute core query patterns.
- Use `explain("executionStats")` for query planning.
- Create and validate indexes.

## Step-by-step hands-on

### Step 1: Prepare environment

From repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Configure environment variables

```powershell
Copy-Item .env.template .env
notepad .env
```

Set:

- `DOCUMENTDB_CONNECTION_STRING`
- `DOCUMENTDB_DATABASE=Workshop_DB`
- Optional Azure OpenAI values for later modules

### Step 3: Validate setup files

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DOCUMENTDB_DATABASE'))"
```

Expected output: `Workshop_DB`

### Step 4: Load workshop data

```powershell
python .\scripts\load_workshop_data.py
python .\scripts\validate_workshop_setup.py
```

### Step 5: Validate collection counts

```powershell
mongosh "<your_connection_string>"
```

```javascript
use Workshop_DB
db.mobiles.countDocuments()
db.supportInc.countDocuments()
db.retail_offers.countDocuments()
```

Expected: `30` for each collection.

### Step 6: Run core queries

```javascript
db.mobiles.find(
  { brand: "Samsung", priceInr: { $lte: 50000 } },
  { _id: 0, title: 1, brand: 1, segment: 1, priceInr: 1, rating: 1 }
).sort({ rating: -1 }).limit(5)
```

```javascript
db.mobiles.find(
  { features: /camera/i, batteryMah: { $gte: 5000 } },
  { _id: 0, title: 1, batteryMah: 1, features: 1 }
).limit(5)
```

### Step 7: Run aggregation framework queries

```javascript
db.mobiles.aggregate([
  {
    $group: {
      _id: "$segment",
      avgPrice: { $avg: "$priceInr" },
      avgRating: { $avg: "$rating" },
      count: { $sum: 1 }
    }
  },
  { $sort: { avgPrice: 1 } }
])
```

### Step 8: Run query planning

```javascript
db.mobiles.find(
  { brand: "Samsung", priceInr: { $lte: 50000 } }
).explain("executionStats")
```

Review `winningPlan`, `totalDocsExamined`, and `executionTimeMillis`.

### Step 9: Create and validate index

```javascript
db.mobiles.createIndex(
  { brand: 1, priceInr: 1 },
  { name: "mobile_brand_price_idx" }
)
```

Re-run explain from Step 8 and compare scan metrics.

## Expected result

You have loaded data, validated queries, run aggregations, and verified index impact through query plans.

## Next module

Continue to:

- `../4-Migration-to-Azure-DocumentDB/README.md`

