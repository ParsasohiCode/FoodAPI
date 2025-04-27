from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()

# Food model using Pydantic
class Food(BaseModel):
    id: Optional[str] = None
    name: str
    price: float
    quantity: int

# In-memory database
foods_db = []

# Create a new food item
@app.post("/foods/", response_model=Food)
async def create_food(food: Food):
    food.id = str(uuid4())
    foods_db.append(food)
    return food

# Get all food items
@app.get("/foods/", response_model=List[Food])
async def get_foods():
    return foods_db

# Get a specific food item
@app.get("/foods/{food_id}", response_model=Food)
async def get_food(food_id: str):
    for food in foods_db:
        if food.id == food_id:
            return food
    raise HTTPException(status_code=404, detail="Food not found")

# Update a food item
@app.put("/foods/{food_id}", response_model=Food)
async def update_food(food_id: str, updated_food: Food):
    for index, food in enumerate(foods_db):
        if food.id == food_id:
            updated_food.id = food_id
            foods_db[index] = updated_food
            return updated_food
    raise HTTPException(status_code=404, detail="Food not found")

# Delete a food item
@app.delete("/foods/{food_id}")
async def delete_food(food_id: str):
    for index, food in enumerate(foods_db):
        if food.id == food_id:
            foods_db.pop(index)
            return {"message": "Food deleted successfully"}
    raise HTTPException(status_code=404, detail="Food not found") 