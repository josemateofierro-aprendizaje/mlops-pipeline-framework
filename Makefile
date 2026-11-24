.PHONY: prepare validate train evaluate pipeline test clean

prepare:
	python -m src.prepare_data

validate:
	python -m src.validate_data

train:
	python -m src.train

evaluate:
	python -m src.evaluate

test:
	python -m pytest tests -v

pipeline:
	python -m src.pipeline --prepare-iris

clean:
	python -c "import shutil; from pathlib import Path; [shutil.rmtree(p) for p in [Path('models'), Path('reports'), Path('data/processed')] if p.exists()]"