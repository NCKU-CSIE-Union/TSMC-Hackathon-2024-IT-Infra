# TSMC Hackathon 2024 IT Infra


## Summary

- **GenAI (Vertex AI + Pinecone)**
  - Analyze Log
  - Store Log and feedback
  - Self-Improved Analyzer progressively
- **Monitor controller**
  - Retrieve Log and Metric
  - Scale Cloud Run Actively
  - The Bridge between GenAI and Discord Bot
- **Discord Bot**
  - Push alert
  - Thread conversation
- **Consumer**
  - Serverless
  - Simulate Scalable Generic Task Consumer
  - Stress Test API to simulate real world scenario
- **Code coverage / TDD**
  - Pytest, High code coverage
- **Wheel CI (aka. build our CI from wheel)**
  - Workflow as Code (yaml format)
  - Github webhook triggered
- **DevOps**
  - Github Action
  - GitFlow
  - CI/CD
  - Docker / Containerization

> System Architecture : <br>
> ![](https://raw.githubusercontent.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/main/docs/system-architecture.png)

## Presentation

> Presentation : <br>
> [![](https://raw.githubusercontent.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/main/docs/pdf-preview.png)](https://github.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/blob/main/2024-TSMC-IT-CareerHack-Presentation.pdf)

<!-- [Final Presentation PDF](https://github.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/blob/main/2024-TSMC-IT-CareerHack-Presentation.pdf) -->

[💡Idea Note](https://github.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/blob/main/docs/Idea.md)

## Authors

- [@HenryChang6](https://www.github.com/HenryChang6)
- [@jason810496](https://www.github.com/jason810496)
- [@jerrykal](https://www.github.com/jerrykal)
- [@peterxcli](https://www.github.com/peterxcli)

## Gitflow

> ![source-tree](https://raw.githubusercontent.com/NCKU-CSIE-Union/TSMC-Hackathon-2024-IT-Infra/main/docs/gitflow.png)

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
