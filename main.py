from typing import Union
import createAbe
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing_extensions import Annotated

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs

CURRENT_ABE = None

class AbeModel(BaseModel):
    user_query: str
    print_relevant_sections: bool
    test_result: bool
    relevant_sections: Union[str, None] = None
    final_answer: Union[str, None] = None
    prompt_cost: Union[str, None] = None

    
    def run_ask_abe(self):
        self.relevant_sections, self.final_answer, self.prompt_cost = createAbe.ask_abe(self.user_query, self.print_relevant_sections, self.test_result)

    def show_sections(self):
        try:
            if self.relevant_sections is None:
                return "Error: Abe has not found relevant sections yet."
            else:
                return self.print_relevant_sections
        except:
            return "Error: Show_sections is not allowed (print_relevant_sections=False)."
        
    def show_answer(self):
        try:
            return self.final_answer
        except:
            return "Error: Abe has not created final answer."
        
    def show_cost(self):
        try:
            return "OpenAI api costs accumulated so far: {}".format(self.prompt_cost)
        except:
            return "Error: Abe has not calculated total prompt costs."
        
app = FastAPI()  

def main():
    pass

@app.post("/abeModel/")
async def create_abe_model(abe: AbeModel):
    abe.run_ask_abe()
    abe_dict = abe.dict()
    CURRENT_ABE = abe
    return abe_dict
    

@app.get("/abeModel/")
async def get_current_abe_model():
    return CURRENT_ABE.dict()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)