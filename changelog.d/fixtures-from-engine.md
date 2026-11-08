### Changed
- `pack.py` and `check_pack.py` build their self-test fixtures under
  `.test-tmp` in the checkout, so both run under a restricted token.
- `check_pack.py` now needs `infra/checks/fixtures.py` beside it.

### Fixed
- The self-test no longer creates `0700` directories it cannot remove;
  a leftover fixture now fails the check that left it.
