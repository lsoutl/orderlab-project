# OrderLab

pytest · Ruff · GitHub Actions 로 CI/CD 를 익히는 실습 프로젝트입니다.
주문 금액 계산 → 할인/배송 규칙 → CSV 매출 집계 → FastAPI 주문 API → 정적 보고서 배포까지 다섯 단계로 확장했습니다.

- 저장소: https://github.com/lsoutl/orderlab-project
- 배포 보고서 (GitHub Pages): https://lsoutl.github.io/orderlab-project/

## 프로젝트 구조

```
orderlab-project/
├── .github/workflows/ci-cd.yml   # lint + test(matrix) + deploy
├── orderlab/
│   ├── pricing.py                # Level 1-2: subtotal, final_total
│   ├── csv_report.py             # Level 3: revenue_from_csv
│   └── api.py                    # Level 4: FastAPI create_app
├── tests/
│   ├── conftest.py               # sample_csv fixture
│   ├── test_pricing.py
│   ├── test_csv_report.py
│   └── test_api.py
├── data/sample_orders.csv
├── generate_report.py            # Level 5: site/index.html 생성
├── requirements-dev.txt
└── pyproject.toml
```

## 로컬 실행

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

ruff check .
ruff format --check .
python -m pytest -q
python -m pytest --cov=orderlab --cov-report=term-missing   # 커버리지
python generate_report.py          # site/index.html 생성
```

## CI/CD 동작 조건

| 이벤트 | lint | test (ubuntu / windows) | deploy |
|---|---|---|---|
| Pull Request → main | 실행 | 실행 | 실행 안 함 (`if: github.event_name == "push"`) |
| Push → main | 실행 | 실행 | lint 와 test 가 모두 PASS 한 경우에만 실행 (`needs`) |

deploy job 은 `generate_report.py` 로 `site/index.html` 을 만들고 GitHub Pages 에 배포합니다.
테스트가 하나라도 FAIL 하면 `needs` 조건 때문에 deploy 는 skipped 가 되어 배포가 차단됩니다.

## 실패 재현 기록

| 단계 | 의도적 실패 | CI 결과 | 수정 |
|---|---|---|---|
| Level 1 | `subtotal(10_000, 2) == 21_000` 으로 기댓값 변경 | `assert 20000 == 21000` FAIL | 기댓값 20_000 복구 |
| Level 1 | `import os` 미사용 import 추가 | Ruff `F401`, `I001` | import 삭제 |
| Level 2 | 배송비 조건을 `amount <= 50_000` 으로 작성 | `test_final_total[50000-1-0-50000]` FAIL (53000 != 50000) | `<` 로 수정 |

## 테스트 셀프 리뷰 체크리스트

- 정상 / 예외 / 경계값 (49,999 · 50,000 · 50,001) 을 모두 다룬다
- 예외는 `pytest.raises` 로, 반복 검증은 `parametrize` 로 작성했다
- 파일 테스트는 `tmp_path` 와 fixture 를 사용해 실제 파일을 건드리지 않는다
- API 테스트는 `create_app()` 으로 매번 새 앱을 만들어 상태를 격리한다
