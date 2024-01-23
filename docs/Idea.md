# TSMC Hackathon 2024

[TOC]

身份證影本
學生證影本
每個參賽者都有裝雙螢幕
可以帶線


Careerhack : hack time
- Resume check 

## Questions

### 1.  training data  

## Cloud Resource

### Cloud Resource Monitering 

:::danger

**Cloud Run** Metrics 研究 : 

:::

### System Log Monitoring 

## Creative

## Presentation 

## Evaluation
![截圖 2024-01-19 下午3.46.54](https://hackmd.io/_uploads/rJzZtivt6.png)


# Idea 

## AI part

## Data analyze
Backend log levels : 
- Warn 
- Fatal 

### Log Input Format
GCP Provide : 
https://cloud.google.com/monitoring/api/metrics_gcp#gcp-run <br>
> time/cpu/ram/req token num/res token num


per timestamp : 
- `timestamp` : timestamp
- `level` : log level
- `cpu` : cpu usage rate
- `ram` : ram usage rate
- `remain_count` : remain query count
- `avg_in_token_count` : average token count
- `avg_out_token_count` : average token count
- `detail` : any detail message

threshold :


### Output Format


### Warn
> CPU , RAM , instance count

### Fatal 
> DC alerting message with details + LLM interative

## Cloud Run Preformance

## Simulate System status

## Completeness

- [AI](#AI)
- [DevOps](#DevOps)
- [Discord Bot](#Discord-Bot)

## Creativity

## Presentation


# Gitflow

### branch
- main
- develop
- feature/xxx
- fix/xxx

### message
feat: 新增/修改功能 (feature)。
fix: 修補 bug (bug fix)。
docs: 文件 (documentation)。
style: 格式 (不影響程式碼運行的變動 white-space, formatting, missing semicolons, etc.)。
refactor: 重構 (既不是新增功能，也不是修補 bug 的程式碼變動)。
perf: 改善效能 (A code change that improves performance)。
test: 增加測試 (when adding missing tests)。
chore: 建構程序或輔助工具的變動 (maintain)。
revert: 撤銷回覆先前的 commit


### folder

- `RAG` : [name=Jerry] AI Part
- `DC-Bot` : [name=Henry] Discord Bot Part
- `Consumer` : [Consumer (Consumer Cloud)](#Consumer-Cloud-Run)
- `MonitorSystem` [Monitor System (GCE)](#Monitor-System-GCE)

# TODO Before Hackathon

- [AI](#AI)
- [DevOps](#DevOps)
- [Monitor System (GCE)](#Monitor-System-GCE)
- [Consumer (Consumer Cloud)](#Consumer-Cloud-Run)
- [Discord Bot](#Service-Discord-Bot)


## AI 

> RAG

## DevOps 
- Flow
    - Git Flow
    - TDD
    - Scrum
- CI / CD 
    - CI
        - [ ] Python Code Quality Check
            - ruff ( lint )
            - [bandit](bandit.readthedocs.io)
        - [x] GCP Image Registry ( Github action )
        - Pytest 
    - CD
        - GCE
        - [x] Cloud Run Deploy ( Github action )
            - Discord Bot notify action update
        - [drone.io](https://www.drone.io/)
            - https://docs.drone.io/server/ha/developer-setup/
            - https://github.com/Jim-Chang/KodingWork/blob/master/devops/painless_set_up_drone_ci_cd/docker-compose.yml
            - https://koding.work/painless-set-up-drone-ci-cd/
            - https://ithelp.ithome.com.tw/articles/10235164
            - https://ithelp.ithome.com.tw/articles/10235165

---

## Consumer (Cloud Run)

==用 counter 來實作 queue 就好, **記得加 lock**==

### Random Generate

- [ ] `remain_count` : remain query count
- [ ] random inference time by:
    - [ ] `avg_in_token_count` : average token count
    - [ ] `avg_out_token_count` : average token count
- [ ] 研究怎麼大量佔用 cpu, mem

### 平常狀態

每個 interval 都先 random(0,1) 看要不要往 queue 塞東西
如果有要塞, 往 queue 裡塞 random(0,N) 個任務

### 開些 API 可以讓系統開始爆炸

範例：
- `/full/cpu?duration=<duration>`
- `/full/ram?duration=<duration>`
- `/full/enqueue?num=<num>`
- `/sleep?duration=<duration>`

### 開些 API 可以達到 xx% 狀態

- `/state/cpu/xx?duration=<duration>`
- `/state/cpu/ram?duration=<duration>`

## Monitor System (GCE)

### Service : Auto scaling

- CPU +-
- RAM +-
- CPU & RAM +-
- Instance Count +-
- instance count +-
    - min = max = current running instance 
- auto get log

reference : 
- [sdk pipy](https://pypi.org/project/google-cloud-run/)
- [github](https://github.com/googleapis/google-cloud-python/tree/main/packages/google-cloud-run)
- [gcloud commad list](https://cloud.google.com/sdk/gcloud/reference/run)
- [gcloud update reference](https://cloud.google.com/sdk/gcloud/reference/run/services/update)
- [ ] python call `gcloud run service update`

### Service : sync log
> for AI input
> call `RAG` afterward

- get current metrics
- get current system log 
- notify Discord Bot 
    - notify DC Bot to send error message

reference : 
[cloud run metrics api](https://cloud.google.com/monitoring/api/metrics_gcp#gcp-run)


### Service: Discord Bot

- [discord bot demo repo](https://github.com/NCKU-CSIE-Union/Discord-Bot-Alert-Bot)
- error 通知
    - [ ] 研究要怎麼讓其他服務主動發通知
    - [ ] 研究 discord broadcast
        - 要怎麼發到指定頻道, 以我們伺服器來說, 要打: `1199009519448109127` 這個 channel
        - 也可以讓使用者主動要求訂閱 (假設使用者在頻道裡打了 `!sub`, 之後有新 alert 就往那些有訂閱的頻道發通知), 用這個做感覺比較好
    - [ ] 漂亮的 Discord 通知 - keyword: `discord embbed message`
- LLM 互動訊息
    - [ ] 收到互動訊息要 call jerry 提供的`answer_question(user_message: str) -> str` function

---

## Test

### Unit Test ( Code Coverage )

### Stress Test

# Tasks

## AI
- Jerry

要幫 system 開 1 個 function
- `insert_log` : 讓 system 可以 sync 當前的 log 到 vertor DB

## Discord Bot
- Henry

## DevOps & Monitor System & Consumer
- Peter
- Jason

