# [how issues go to the md?](https://github.com/SylverQG/Blogs/issues/2)

1. 本仓库搭建概况
   - 基于 [https://github.com/yihong0618/gitblog/issues/177](https://github.com/yihong0618/gitblog/issues/177) 、
   - 加上 [https://github.com/egolearner/paper-note.git](https://github.com/egolearner/paper-note.git) 的一些配置(Action自动化), 
   - 并更新到较新的`ActionFlow`版本(当然应该不是最合适的版本，好像还是有`Node.js 12 to Node.js 16` 的警告)

2. 搭建过程的一些问题(遇到的，并从issue里总结的)
   1. cookbook依旧是[https://github.com/yihong0618/gitblog/issues/177](https://github.com/yihong0618/gitblog/issues/177)中的这些步骤，即
      - ①生成个人Token，并添加到仓库设置中。
      - ②文件`.github/workflows/generate_readme.yml`中`env`项的`name`和`email`设置更改为自己的
   2. `.github/workflows/generate_readme.yml`的其他修改如下：即添加注释的地方
    ```yml
        name: Generate README
        
        on:
          issues:
            types: [opened, edited]
          issue_comment:
            types: [created, edited]
          push:
            branches:
              - main
            paths:
              - main.py
        
        env:
          GITHUB_NAME: SylverQG
          GITHUB_EMAIL: doublc_qluv@163.com
        
        jobs:
          sync:
            name: Generate README
            runs-on: ubuntu-latest
            if: github.repository_owner_id == github.event.issue.user.id || github.event_name == 'push'
            steps:
              - name: Checkout
                uses: actions/checkout@v3
              - name: Set up Python
                uses: actions/setup-python@v3
                with:
                  python-version: 3.9
                  cache: pip
                  cache-dependency-path: "requirements.txt"
        
              # - name: Configure pip cache
              #   uses: actions/cache@v2
              #   id: pip-cache
              #   with:
              #     path: venv
              #     key: pip-1-${{ "hashFiles('**/requirements.txt')" }}
              #     restore-keys: |
              #       pip-
              
              - name: Install dependencies
                run: |
                  python -m pip install --upgrade pip
                  python -m venv venv
                  source venv/bin/activate
                  pip install -r requirements.txt
                # if: steps.pip-cache.outputs.cache-hit != 'true'
              
              - name: Generate new md
                run: |
                  source venv/bin/activate
                  python main.py ${{ secrets.G_T }} ${{ github.repository }} --issue_number '${{ github.event.issue.number }}'
        
              # - name: Push README
              #   uses: github-actions-x/commit@v2.9
              #   with:
              #     github-token: ${{ secrets.G_T }}
              #     commit-message: "UPDATE README"
              #     files: BACKUP/*.md README.md feed.xml
              #     rebase: 'true'
              #     name: SylverQG 
              #     email: doublc_qluv@163.com
        
              - name: Push README
                run: |
                  git config --local user.email "${{ env.GITHUB_EMAIL }}"
                  git config --local user.name "${{ env.GITHUB_NAME }}"
                  git add BACKUP/*.md
                  git commit -a -m 'update new blog' || echo "nothing to commit"
                  git push || echo "nothing to push"
    ```
 3. 警告详情 `actions/checkout@v2`,`actions/setup-python@v1`,`actions/cache@v1`  update to `actions/checkout@v3`,`actions/setup-python@v2`,`actions/cache@v2` 
```Warning
Generate README
Node.js 12 actions are deprecated. Please update the following actions to use Node.js 16: actions/setup-python@v2, actions/cache@v2. For more information see: https://github.blog/changelog/2022-09-22-github-actions-all-actions-will-begin-running-on-node16-instead-of-node12/.
```
   4. 错误详情 `github-actions-x/commit@v2.6` update to v2.9 (the latest)
the error shows:

```error
Command line: | /usr/bin/git pull --rebase --autostash origin main
Stderr:       | fatal: detected dubious ownership in repository at '/github/workspace'
              | To add an exception for this directory, call:
              | 
              | 	git config --global --add safe.directory /github/workspace
```
   5. 错误详情 `生成通过但是仓库没有变更` ，此时可以重新生成Token，重新添加到仓库的设置中。[这与本地的错误类似，即没有当前仓库的权限]
```error
remote: Permission to SylverQG/Blogs.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/SylverQG/Blogs/': The requested URL returned error: 403
nothing to push
```