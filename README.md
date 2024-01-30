# TSMC Hackathon 2024 IT Infra

> [!IMPORTANT]
> We use **`Poetry`** to manage python package and virtual environment !!!

<!-- 
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts
 -->

## Summary

- GenAI (Vertex AI + Pinecone)
  - Analyze Log
  - Store Log and feedback
  - Self-Improved Analyzer progressively
- monitor controller
  - Retrieve Log and Metric
  - Scale Cloud Run Actively
  - The Bridge between GenAI and Discord Bot
- Discord Bot
  - Push alert
  - Thread conversation
- Consumer
  - Serverless
  - Simulate Scalable Generic Task Consumer
  - Stress Test API to simulate real world scenario
- Code coverage / TDD
  - Pytest, High code coverage
- Wheel CI (aka. build our CI from wheel)
  - Workflow as Code (yaml format)
  - Github webhook triggered
- DevOps
  - Github Action
  - GitFlow
  - CI/CD
  - Docker / Containerization

## Idea Note

<!-- ## TODO

- [AI](#AI)
- [DevOps](#DevOps)
- [Monitor System (GCE)](#Monitor-System-GCE)
- [Consumer (Consumer Cloud)](#Consumer-Cloud-Run)
- [Discord Bot](#Service-Discord-Bot) -->

## Gitflow

### branch

- main
- develop
- test
- document
- feature/xxx
- fix/xxx
- hotfix/xxx

### message

- feat: 新增/修改功能 (feature)。
- fix: 修補 bug (bug fix)。
- docs: 文件 (documentation)。
- style: 格式 (不影響程式碼運行的變動 white-space, formatting, missing semicolons, etc.)。
- refactor: 重構 (既不是新增功能，也不是修補 bug 的程式碼變動)。
- perf: 改善效能 (A code change that improves performance)。
- test: 增加測試 (when adding missing tests)。
- chore: 建構程序或輔助工具的變動 (maintain)。
- revert: 撤銷回覆先前的 commit
- ci: DevOps 相關設定
