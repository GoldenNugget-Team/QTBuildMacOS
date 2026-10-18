# QTBuildMacOS

Общая сборка Qt для проектов GoldenNugget-Team. Готовые wheel-пакеты
публикуются в [Releases](https://github.com/GoldenNugget-Team/QTBuildMacOS/releases).
Проектам не нужно заново компилировать Qt при каждой сборке приложения.

Текущая конфигурация:

| Компонент | Версия / параметры |
| --- | --- |
| Qt, PySide6, Shiboken6 | 6.12.0 |
| Python | CPython 3.15, ABI cp315 |
| Архитектуры | Universal2: arm64 + x86_64 |
| Минимальная macOS | 14.4 Sonoma |
| Модули | Core, Gui, Widgets, Network, Svg |
| Runner сборки | macos-26, Apple Silicon |
| Релиз | `qt-6.12.0-python-3.15-macos-14.4-v1` |

## Подключение GitHub Actions

```yaml
jobs:
  qt:
    uses: GoldenNugget-Team/QTBuildMacOS/.github/workflows/download.yml@main
    permissions:
      contents: read

  build:
    needs: qt
    runs-on: macos-26
    steps:
      - uses: actions/checkout@v5
      - uses: actions/download-artifact@v7
        with:
          name: macOS-Qt-universal2
          path: .macos-qt-wheels
      # Сначала установите universal2 Python 3.15 и создайте venv.
      - run: python -m pip install --no-deps .macos-qt-wheels/*.whl
```

Для воспроизводимой конфигурации замените `@main` на SHA коммита общего
репозитория. Необязательные inputs `release` и `artifact-name` позволяют
выбрать релиз и имя артефакта. Workflow скачивает пакеты из общего публичного
релиза, проверяет SHA256 и передаёт их в артефакт текущего запуска.
Дополнительный PAT не требуется.

Можно скачать пакеты напрямую:

```sh
gh release download qt-6.12.0-python-3.15-macos-14.4-v1 \
  --repo GoldenNugget-Team/QTBuildMacOS \
  --pattern '*.whl' --pattern SHA256SUMS.txt --dir wheels
cd wheels
shasum -a 256 -c SHA256SUMS.txt
python -m pip install --no-deps ./*.whl
```

Wheel-тег `macosx_14_0_universal2` учитывает правила тегов Python packaging.
Фактический минимум Mach-O остаётся 14.4; нормализация изменяет только
метаданные wheel. Используйте Python 3.15 на macOS 14.4 или новее.
Пакеты не подходят для Python 3.13 и не содержат Qt Designer/Assistant/Linguist.
Ресурсы и переводы приложения должны быть скомпилированы заранее.

## Пересборка

Запустите **Build shared macOS Qt** вручную в Actions. Workflow устанавливает
universal2 Python 3.15.0, собирает QtBase/QtSvg и Python bindings, проверяет
обе архитектуры всех Mach-O файлов, устанавливает пакеты и выполняет smoke-тест.
После проверки он публикует wheel-пакеты и `SHA256SUMS.txt`.

Опубликованный релиз не перезаписывается. Перед новой публикацией обновите
тег `QT_RELEASE` в `build.yml`, default релиза в `download.yml` и документацию.
Версии Qt/Python меняются согласованно в скрипте, workflow и smoke-тесте.
Сборка запускается вручную, чтобы изменение документации или потребителя
не запускало длительную компиляцию.

Для локальной сборки нужны Apple Silicon, Xcode Command Line Tools,
Homebrew и universal2 Python 3.15 в активном venv:

```sh
bash tools/build_macos_qt.sh
```

Параметры окружения: `QT_BUILD_JOBS` (число задач компилятора),
`QT_BUILD_ROOT` (новая папка сборки), `QT_WHEELS_DIR` (папка результата,
по умолчанию `.macos-qt-wheels`). Сохраняется совместимость с
`GOLDENNUGGET_BUILD_JOBS`. Повторная сборка требует новой или очищенной
папки исходников; кешируются готовые wheels.

Первый релиз перенесён из успешного запуска
[GoldenNugget #39126137170](https://github.com/GoldenNugget-Team/GoldenNugget/actions/runs/39126137170).
При переносе нормализованы метаданные, проверены архитектуры и выполнены
smoke-тесты. Бинарное содержимое исходных wheel-пакетов сохраняется.

## Лицензии

Скрипты перенесены из GoldenNugget и распространяются под AGPL-3.0
(см. `LICENSE`). Qt, PySide6 и Shiboken6 сохраняют собственные лицензии
и уведомления, включённые в дистрибутивы. При распространении приложений
учитывайте условия используемых компонентов Qt.
