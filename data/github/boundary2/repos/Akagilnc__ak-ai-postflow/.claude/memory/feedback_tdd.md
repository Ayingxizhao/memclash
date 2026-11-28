---
name: TDD workflow requirement
description: User requires Test-Driven Development — write tests before or alongside implementation, not as afterthought
type: feedback
---

Always follow TDD when adding features. Write tests first or at minimum alongside the implementation code.

**Why:** User explicitly called out forgetting TDD when tests were added as an afterthought after multiple features were already implemented.

**How to apply:** Before implementing a new function, write the test case first. Commit tests with the feature, not in a separate "补测试" commit.
