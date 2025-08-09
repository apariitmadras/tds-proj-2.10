from pydantic import BaseModel, Field
from typing import List, Dict, Any

class EP(BaseModel):
    meta: Dict[str, Any]
    io: Dict[str, Any]
    questions: List[Dict[str, Any]]
    data_sources: List[Dict[str, Any]]
    parsing_rules: Dict[str, Any]
    computations: List[Dict[str, Any]]
    tool_plan: List[Dict[str, Any]]
    validations: List[str]

class CodePackage(BaseModel):
    language: str
    entrypoint: str
    stdout_contract: str
    code: str
