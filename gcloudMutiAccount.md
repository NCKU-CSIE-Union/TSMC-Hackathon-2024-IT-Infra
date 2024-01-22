# Using `gcloud` with multiple accounts


> Jump to : [Switch account command](#switch-between-config--account)

## create new config

```
gcloud config configurations create YOUR_CONFIG_NAME
```
> Created [demo-config].
> Activated [demo-config].


## set project and account

```
gcloud config set project my-project-id
```
> Updated property [core/project].

```
gcloud config set account my-account@example.com
```
> Updated property [core/account].

## login with new config account

```
gcloud auth login
```

## switch between config ( account )
```
gcloud config configurations list # list all config

gcloud config configurations activate YOUR_CONFIG_NAME
```

## reference
https://medium.com/google-cloud/how-to-use-multiple-accounts-with-gcloud-848fdb53a39a