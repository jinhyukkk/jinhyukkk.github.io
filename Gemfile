source "https://rubygems.org"

# GitHub Pages(github-pages 232)와 같은 버전으로 로컬 빌드.
# github-pages 메타 gem은 jekyll-remote-theme → openssl 네이티브 빌드가 Windows에서 실패해 쓰지 않음.
# shortcut: 버전을 손으로 맞춤, https://pages.github.com/versions/ 가 바뀌면 함께 갱신
gem "jekyll", "3.10.0"
gem "kramdown", "2.4.0"
gem "kramdown-parser-gfm", "1.1.0"
gem "rouge", "3.30.0"
gem "webrick"

group :jekyll_plugins do
  gem "jekyll-feed", "0.17.0"
  gem "jekyll-sitemap", "1.4.0"
  gem "jekyll-seo-tag", "2.8.0"
end

# Windows 로컬 빌드용
platforms :mingw, :x64_mingw, :mswin do
  gem "tzinfo-data"
  gem "wdm"
end
