install:
	uv sync
	
start:
	uvicorn main:app --reload

