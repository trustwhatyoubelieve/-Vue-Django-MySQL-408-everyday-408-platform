/**
 * question_bank/static/question_bank/admin.js
 * ============================================
 * Django Admin 联动下拉逻辑，实现：
 *   A. SubChapterAdmin: 选课程 → 自动过滤章节下拉
 *   B. QuestionAdmin  : 选课程 → 自动过滤章节 → 自动过滤子章节
 *
 * 无需 jQuery，直接使用原生 JS + Django Admin 的 DOM 结构。
 * 自动处理新增页和编辑页。
 */

(function () {
    'use strict';

    // ===================================================================
    // 通用工具
    // ===================================================================

    /**
     * 等待 DOM ready
     * @param {Function} callback
     */
    function domReady(callback) {
        if (document.readyState !== 'loading') {
            callback();
        } else {
            document.addEventListener('DOMContentLoaded', callback);
        }
    }

    /**
     * 根据 id 获取 DOM 元素，找不到返回 null
     * @param {string} id
     * @returns {HTMLElement|null}
     */
    function $ (id) {
        return document.getElementById(id);
    }

    /**
     * 清空 select 所有选项，并保留一个空选项（可选 label）
     * @param {HTMLSelectElement} selectEl
     * @param {string}           emptyLabel
     */
    function clearSelect(selectEl, emptyLabel) {
        selectEl.innerHTML = '';
        var opt = document.createElement('option');
        opt.value = '';
        opt.textContent = emptyLabel || '---------';
        selectEl.appendChild(opt);
        selectEl.disabled = true;
    }

    /**
     * 向 select 填充选项列表
     * @param {HTMLSelectElement} selectEl
     * @param {Array}             items     [{id, name}]
     * @param {boolean}           disabled  填充后是否禁用
     */
    function populateSelect(selectEl, items, disabled) {
        selectEl.innerHTML = '';
        var defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.textContent = '---------';
        selectEl.appendChild(defaultOpt);

        items.forEach(function (item) {
            var opt = document.createElement('option');
            opt.value = item.id;
            opt.textContent = item.name;
            selectEl.appendChild(opt);
        });

        selectEl.disabled = (disabled === true) || items.length === 0;
    }

    /**
     * 从指定 URL 获取 JSON 数据
     * @param {string}   url
     * @param {Function} onSuccess  (data) => void
     * @param {Function} onError    (err)  => void
     */
    function fetchJSON(url, onSuccess, onError) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    onSuccess(JSON.parse(xhr.responseText));
                } catch (e) {
                    onError(e);
                }
            } else {
                onError(new Error('HTTP ' + xhr.status));
            }
        };
        xhr.onerror = function () { onError(new Error('Network error')); };
        xhr.send();
    }


    // ===================================================================
    // 联动接口
    // 路由到 /admin/question_bank/chapter/by-course/<course_id>/
    //        /admin/question_bank/subchapter/by-chapter/<chapter_id>/
    // 需要在 admin.py 中注册对应的 URL。
    // ===================================================================

    /**
     * 根据课程 ID 获取章节列表
     * @param {number}   courseId
     * @param {Function} callback  (items) => void
     */
    function loadChaptersByCourse(courseId, callback) {
        if (!courseId) {
            callback([]);
            return;
        }
        var url = '/admin/question_bank/chapter/by-course/' + courseId + '/';
        fetchJSON(url, function (data) { callback(data.chapters || []); }, function () { callback([]); });
    }

    /**
     * 根据章节 ID 获取子章节列表
     * @param {number}   chapterId
     * @param {Function} callback  (items) => void
     */
    function loadSubChaptersByChapter(chapterId, callback) {
        if (!chapterId) {
            callback([]);
            return;
        }
        var url = '/admin/question_bank/subchapter/by-chapter/' + chapterId + '/';
        fetchJSON(url, function (data) { callback(data.subchapters || []); }, function () { callback([]); });
    }


    // ===================================================================
    // 绑定器：SubChapterAdmin（课程 → 章节 联动）
    // ===================================================================

    function bindSubChapterForm() {
        var courseEl     = $('id_course_filter');
        var chapterEl    = $('id_chapter');

        if (!courseEl || !chapterEl) return;

        // 课程切换时：加载章节列表
        courseEl.addEventListener('change', function () {
            var courseId = parseInt(courseEl.value, 10);
            if (!courseId) {
                clearSelect(chapterEl, '—— 请先选择课程 ——');
                return;
            }
            loadChaptersByCourse(courseId, function (chapters) {
                populateSelect(chapterEl, chapters);
            });
        });

        // 编辑页：若课程已有初始值，手动触发一次加载
        if (courseEl.value) {
            courseEl.dispatchEvent(new Event('change'));
        }
    }


    // ===================================================================
    // 绑定器：QuestionAdmin（课程 → 章节 → 子章节 三级联动）
    // ===================================================================

    function bindQuestionForm() {
        var courseEl     = $('id_course_filter');
        var chapterEl    = $('id_chapter_filter');
        var subchapterEl = $('id_subchapter');

        if (!courseEl || !chapterEl || !subchapterEl) return;

        // 课程切换 → 刷新章节，并清空子章节
        courseEl.addEventListener('change', function () {
            var courseId = parseInt(courseEl.value, 10);
            if (!courseId) {
                clearSelect(chapterEl,    '—— 请先选择课程 ——');
                clearSelect(subchapterEl, '—— 请先选择章节 ——');
                return;
            }
            loadChaptersByCourse(courseId, function (chapters) {
                populateSelect(chapterEl, chapters);
                clearSelect(subchapterEl, '—— 请先选择章节 ——');
                // 若只有唯一章节，自动触发加载子章节
                if (chapters.length === 1) {
                    chapterEl.value = chapters[0].id;
                    chapterEl.dispatchEvent(new Event('change'));
                }
            });
        });

        // 章节切换 → 加载子章节
        chapterEl.addEventListener('change', function () {
            var chapterId = parseInt(chapterEl.value, 10);
            if (!chapterId) {
                clearSelect(subchapterEl, '—— 请先选择章节 ——');
                return;
            }
            loadSubChaptersByChapter(chapterId, function (subchapters) {
                populateSelect(subchapterEl, subchapters);
            });
        });

        // 编辑页：若已有初始值，手动触发级联
        if (courseEl.value) {
            courseEl.dispatchEvent(new Event('change'));
        }
    }


    // ===================================================================
    // 入口
    // ===================================================================

    domReady(function () {
        bindSubChapterForm();
        bindQuestionForm();
    });

})();
