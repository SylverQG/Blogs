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

好像是仓库的[Actions secrets](https://github.com/SylverQG/Blogs/settings/secrets/actions) 中的`G_T`过期了，从而导致的错误