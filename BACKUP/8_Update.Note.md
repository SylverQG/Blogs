# [Update Note](https://github.com/SylverQG/Blogs/issues/8)

我更新了一下Action里面需要的版本，似乎又make了，因为我重新看了一下仓库issues的更新的提示[https://github.com/yihong0618/gitblog/issues/177](https://github.com/yihong0618/gitblog/issues/177)需要把Backup文件夹[删除](https://github.com/SylverQG/Blogs/commit/46b48b5f693df83812deef9d5abbd857ce963b25)。

再次复制一下整个的[`yml`](https://github.com/SylverQG/Blogs/blob/main/.github/workflows/generate_readme.yml)

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
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.13
          cache: pip
          cache-dependency-path: "requirements.txt"
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt
      
      - name: Generate new md
        run: |
          source venv/bin/activate
          python main.py ${{ secrets.G_T }} ${{ github.repository }} --issue_number '${{ github.event.issue.number }}'

      - name: Push README
        run: |
          git config --local user.email "${{ env.GITHUB_EMAIL }}"
          git config --local user.name "${{ env.GITHUB_NAME }}"
          git add BACKUP/*.md
          git commit -a -m 'update new blog' || echo "nothing to commit"
          git push || echo "nothing to push"
```

---

> 好像是仓库的[Actions secrets](https://github.com/SylverQG/Blogs/settings/secrets/actions) 中的`G_T`过期了，从而导致的错误,
>> 在 [这里](https://github.com/settings/tokens) 重新生成一个`token`，然后复制过去就好

```bash
Run source venv/bin/activate
  source venv/bin/activate
  python main.py *** SylverQG/Blogs --issue_number '8'
  shell: /usr/bin/bash -e {0}
  env:
    GITHUB_NAME: SylverQG
    GITHUB_EMAIL: doublc_qluv@163.com
    pythonLocation: /opt/hostedtoolcache/Python/3.13.5/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.13.5/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.5/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.5/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.13.5/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.13.5/x64/lib
Traceback (most recent call last):
  File "/home/runner/work/Blogs/Blogs/main.py", line 320, in <module>
    main(options.github_token, options.repo_name, options.issue_number)
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/Blogs/Blogs/main.py", line 281, in main
    me = get_me(user)
  File "/home/runner/work/Blogs/Blogs/main.py", line 34, in get_me
    return user.get_user().login
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/AuthenticatedUser.py", line 293, in login
    self._completeIfNotSet(self._login)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/GithubObject.py", line 559, in _completeIfNotSet
    self._completeIfNeeded()
    ~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/GithubObject.py", line 563, in _completeIfNeeded
    self.__complete()
    ~~~~~~~~~~~~~~~^^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/GithubObject.py", line 568, in __complete
    headers, data = self._requester.requestJsonAndCheck("GET", self._url.value, headers=self.__completeHeaders)
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/Requester.py", line 622, in requestJsonAndCheck
    return self.__check(
           ~~~~~~~~~~~~^
        *self.requestJson(
        ^^^^^^^^^^^^^^^^^^
    ...<7 lines>...
        )
        ^
    )
    ^
  File "/home/runner/work/Blogs/Blogs/venv/lib/python3.13/site-packages/github/Requester.py", line 790, in __check
    raise self.createException(status, responseHeaders, data)
github.GithubException.BadCredentialsException: 401 {"message": "Bad credentials", "documentation_url": "https://docs.github.com/rest", "status": "401"}
Error: Process completed with exit code 1.
```


> 新的报错是在`main.py`中做一下修改就好

```bash
File "/home/runner/work/Blogs/Blogs/main.py", line 118, in get_issues_from_label
  return repo.get_issues(labels=(label,))
         ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
...
AssertionError: (Label(name="C/C++"),)
```

错误发生在get_issues_from_label函数中。PyGithub 库要求：

1. labels参数必须是​​列表 (list)​​ 格式
2. 您目前使用的是​​元组 (tuple)​​ 格式 (label,)
3. 标签名包含特殊字符C/C++时更容易触发此错误

>> 修复方案：​​修改 get_issues_from_label函数​​ (约在118行)

```python
# 修改前
return repo.get_issues(labels=(label,))

# 修改后
return repo.get_issues(labels=[label])
```