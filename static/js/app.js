/**
 * Free Music - 前端交互逻辑
 * 优化版：强制歌手+歌曲名、播放下载分离、美化UI交互
 */

// ==================== 全局变量 ====================
let currentPlaylist = [];
let currentTrackIndex = -1;
let isPlaying = false;
let currentFilename = '';
let currentTempFile = null; // 记录当前临时文件，播放结束后清理

// DOM元素
const elements = {
    // 搜索相关
    artistInput: document.getElementById('artistInput'),
    songInput: document.getElementById('songInput'),
    searchBtn: document.getElementById('searchBtn'),
    searchResults: document.getElementById('searchResults'),
    resultsList: document.getElementById('resultsList'),
    resultCount: document.getElementById('resultCount'),
    searchLoading: document.getElementById('searchLoading'),
    
    // 音乐库相关
    libraryList: document.getElementById('libraryList'),
    libraryEmpty: document.getElementById('libraryEmpty'),
    refreshLibraryBtn: document.getElementById('refreshLibraryBtn'),
    
    // 播放器相关
    playerBar: document.getElementById('playerBar'),
    audioPlayer: document.getElementById('audioPlayer'),
    playPauseBtn: document.getElementById('playPauseBtn'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    currentSongTitle: document.getElementById('currentSongTitle'),
    currentSongArtist: document.getElementById('currentSongArtist'),
    albumCover: document.getElementById('albumCover'),
    progressSlider: document.getElementById('progressSlider'),
    progressFill: document.getElementById('progressFill'),
    progressHandle: document.getElementById('progressHandle'),
    currentTime: document.getElementById('currentTime'),
    totalTime: document.getElementById('totalTime'),
    volumeBtn: document.getElementById('volumeBtn'),
    volumeSlider: document.getElementById('volumeSlider'),
    downloadCurrentBtn: document.getElementById('downloadCurrentBtn'),
    
    // 通知
    notification: document.getElementById('notification'),
};

// ==================== 页面初始化 ====================
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    initAudioPlayer();
    checkUserStatus(); // 检查用户登录状态
    loadLibrary(); // 自动加载曲库
});

// ==================== 事件监听器 ====================
function initEventListeners() {
    // 导航切换
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchTab(link.dataset.tab);
        });
    });
    
    // 搜索
    elements.searchBtn.addEventListener('click', handleSearch);
    elements.artistInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') elements.songInput.focus();
    });
    elements.songInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
    
    // 音乐库刷新
    elements.refreshLibraryBtn.addEventListener('click', loadLibrary);
    
    // 播放器控制
    elements.playPauseBtn.addEventListener('click', togglePlayPause);
    elements.prevBtn.addEventListener('click', playPrevious);
    elements.nextBtn.addEventListener('click', playNext);
    elements.downloadCurrentBtn.addEventListener('click', downloadCurrentSong);
    
    // 进度条
    elements.progressSlider.addEventListener('input', (e) => {
        const time = (e.target.value / 100) * elements.audioPlayer.duration;
        elements.audioPlayer.currentTime = time;
        updateProgressVisual();
    });
    
    // 音量控制
    elements.volumeSlider.addEventListener('input', (e) => {
        elements.audioPlayer.volume = e.target.value / 100;
        updateVolumeIcon(e.target.value);
    });
    
    elements.volumeBtn.addEventListener('click', toggleMute);
}

// ==================== 标签页切换 ====================
function switchTab(tabName) {
    // 更新导航链接
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.tab === tabName) {
            link.classList.add('active');
        }
    });
    
    // 更新内容区域
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // 加载对应数据
    if (tabName === 'library') {
        loadLibrary();
    }
}

// ==================== 搜索功能 ====================
async function handleSearch() {
    const artist = elements.artistInput.value.trim();
    const song = elements.songInput.value.trim();
    
    // 严格验证：必须同时输入歌手名和歌曲名
    if (!artist && !song) {
        showNotification('⚠️ 请输入歌手名和歌曲名', 'error');
        elements.artistInput.focus();
        return;
    }
    
    if (!artist) {
        showNotification('⚠️ 请输入歌手名', 'error');
        elements.artistInput.focus();
        return;
    }
    
    if (!song) {
        showNotification('⚠️ 请输入歌曲名', 'error');
        elements.songInput.focus();
        return;
    }
    
    // 长度验证
    if (artist.length < 2 || song.length < 2) {
        showNotification('⚠️ 歌手名和歌曲名至少需要2个字符', 'error');
        return;
    }
    
    const keyword = `${artist} ${song}`;
    
    // 显示加载动画
    elements.searchLoading.style.display = 'block';
    elements.searchResults.style.display = 'none';
    elements.searchBtn.disabled = true;
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                keyword,
                artist,
                song
            }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.data.length === 0) {
                showNotification(`🔍 未找到「${artist} - ${song}」相关音乐，请尝试其他关键词`, 'error');
                elements.searchResults.style.display = 'none';
            } else {
                displaySearchResults(data.data, artist, song);
                showNotification(`✅ 找到 ${data.total} 首相关音乐`, 'success');
            }
        } else {
            showNotification(`❌ ${data.message || '搜索失败'}`, 'error');
            elements.searchResults.style.display = 'none';
        }
    } catch (error) {
        console.error('搜索错误:', error);
        showNotification('❌ 搜索失败，请检查网络连接', 'error');
    } finally {
        elements.searchLoading.style.display = 'none';
        elements.searchBtn.disabled = false;
    }
}

// ==================== 显示搜索结果 ====================
function displaySearchResults(results, artist, song) {
    elements.resultsList.innerHTML = '';
    elements.resultCount.textContent = results.length;
    
    results.forEach((item, index) => {
        const musicItem = createMusicItem(item, index, 'search', artist, song);
        elements.resultsList.appendChild(musicItem);
    });
    
    elements.searchResults.style.display = 'block';
    
    // 保存当前播放列表
    currentPlaylist = results;
}

// ==================== 创建音乐列表项 ====================
function createMusicItem(item, index, source, artist = '', song = '') {
    const div = document.createElement('div');
    div.className = 'music-item';
    
    // 处理标题显示
    const displayTitle = formatMusicTitle(item.title || item.name, artist, song);
    const scoreClass = item.score >= 70 ? 'score-badge' : '';
    
    div.innerHTML = `
        <span class="music-index">${index + 1}</span>
        <div class="music-cover">🎵</div>
        <div class="music-info">
            <div class="music-title">${escapeHtml(displayTitle)}</div>
            <div class="music-meta">
                ${item.author ? `<span>🎤来源 ${escapeHtml(item.author)}</span>` : ''}
                ${item.duration ? `<span>⏱️ ${item.duration}</span>` : ''}
                ${item.score ? `<span class="${scoreClass}">🎯 ${item.score}分</span>` : ''}
            </div>
        </div>
        <div class="music-actions">
            ${source === 'search' ? `
                <button class="btn btn-success btn-small" onclick="playMusic('${escapeAttr(item.video_url)}', '${escapeAttr(displayTitle)}', '${escapeAttr(item.author || artist)}', ${index})">
                    <span class="btn-icon">▶️</span>
                    <span class="btn-text">播放</span>
                </button>
            ` : `
                <button class="btn btn-primary btn-small play-from-library-btn" data-index="${index}">
                    <span class="btn-icon">▶️</span>
                    <span class="btn-text">播放</span>
                </button>
                <button class="btn btn-danger btn-small" onclick="deleteMusic(${item.id})">
                    <span class="btn-icon">🗑️</span>
                    <span class="btn-text">删除</span>
                </button>
            `}
        </div>
    `;
    
    return div;
}

// ==================== 格式化音乐标题 ====================
function formatMusicTitle(title, artist, song) {
    // 清理HTML标签和特殊字符
    let cleaned = title.replace(/<[^>]*>/g, '').replace(/&[a-z]+;/gi, '');
    
    // 如果标题过长，尝试提取核心信息
    if (cleaned.length > 50) {
        // 移除常见的无用信息
        cleaned = cleaned
            .replace(/\[.*?\]/g, '') // 移除方括号内容
            .replace(/【.*?】/g, '') // 移除中文方括号
            .replace(/\(.*?官方.*?\)/gi, '') // 移除官方标记
            .replace(/\s+/g, ' ') // 合并空格
            .trim();
    }
    
    // 如果有歌手和歌曲名，尝试构建标准格式
    if (artist && song && cleaned.includes(song)) {
        return `${artist} - ${song}`;
    }
    
    return cleaned;
}

// ==================== 播放音乐（搜索结果） ====================
async function playMusic(videoUrl, title, artist, index) {
    console.log('🎵 playMusic 被调用');
    console.log('  - videoUrl:', videoUrl);
    console.log('  - title:', title);
    console.log('  - artist:', artist);
    console.log('  - index:', index);
    
    // 防止重复操作 - 使用更智能的锁机制
    const lockKey = `${videoUrl}_${title}`;
    if (window.currentProcessingLock === lockKey) {
        console.warn('⚠️ 相同的音乐正在处理中，跳过');
        showNotification('⚠️ 正在处理中，请稍候...', 'info');
        return;
    }
    
    window.currentProcessingLock = lockKey;
    
    try {
        // 构建安全文件名
        const safeTitle = title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5\s\-]/g, '').trim();
        const safeArtist = artist.replace(/[^a-zA-Z0-9\u4e00-\u9fa5\s\-]/g, '').trim();
        
        console.log('📁 安全处理后的标题:', safeTitle);
        console.log('📁 安全处理后的歌手:', safeArtist);
        
        // 每次都重新下载，不使用缓存
        showNotification('🚀 正在从 B 站下载音频...', 'info');
        console.log('📥 开始下载音频...');
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            console.error('⏱️ 请求超时（120秒）');
            controller.abort();
        }, 120000);
        
        const response = await fetch('/api/cache', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_url: videoUrl,
                title: safeTitle,
                artist: safeArtist
            }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log('📡 收到服务器响应:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ HTTP错误:', response.status, errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('📦 响应数据:', data);
        console.log('🔍 检查数据结构:');
        console.log('  - data.success:', data.success);
        console.log('  - data.data:', data.data);
        if (data.data) {
            console.log('  - data.data.filename:', data.data.filename);
            console.log('  - data.data.play_url:', data.data.play_url);
            console.log('  - data.data.temp_file:', data.data.temp_file);
        }
        
        if (data.success) {
            currentTrackIndex = index;
            currentFilename = data.data.filename;
            
            // 如果是临时文件，记录下来
            if (data.data.temp_file) {
                currentTempFile = data.data.filename;
                console.log('📁 记录临时文件:', currentTempFile);
            }
            
            console.log('✅ 下载成功，准备播放');
            console.log('  - 文件名:', currentFilename);
            console.log('  - 播放URL:', data.data.play_url);
            
            // 播放
            playFromUrl(data.data.play_url, title, artist);
            showNotification('✅ 下载完成，开始播放', 'success');
            
            // 刷新音乐库
            setTimeout(() => loadLibrary(), 1000);
            
            // 显示下载按钮
            elements.downloadCurrentBtn.style.display = 'flex';
        } else {
            console.error('❌ 服务器返回失败:', data.message);
            showNotification(`❌ ${data.message || '播放失败'}`, 'error');
        }
    } catch (error) {
        console.error('❌ playMusic 异常:', error);
        if (error.name === 'AbortError') {
            showNotification('❌ 请求超时，音频文件可能较大，请稍后重试', 'error');
        } else {
            showNotification(`❌ 播放失败: ${error.message}`, 'error');
        }
    } finally {
        window.currentProcessingLock = null;
        console.log('🔓 处理锁已释放');
    }
}

// ==================== 从曲库播放 ====================
async function playFromLibrary(index, item) {
    // 曲库现在只有元数据，需要重新下载
    console.log('📚 从曲库/歌单播放:', item.title || item.name);
    console.log('  - video_url:', item.video_url);
    console.log('  - index:', index);
    
    // 兼容搜索结果(author)和曲库数据(artist)
    const artist = item.artist || item.author || '';
    const title = item.title || item.name || '未知歌曲';
    
    // 使用 playMusic 函数重新下载并播放
    await playMusic(item.video_url, title, artist, index);
}

// ==================== 从URL播放 ====================
function playFromUrl(url, title, artist = '') {
    console.log('🎵 准备播放音乐:');
    console.log('  - URL:', url);
    console.log('  - 标题:', title);
    console.log('  - 歌手:', artist);
    
    // 显示播放器栏
    if (elements.playerBar) {
        elements.playerBar.classList.add('visible');
        console.log('✅ 播放器栏已显示');
    }
    
    // 重置播放器状态
    elements.audioPlayer.pause();
    elements.audioPlayer.currentTime = 0;
    
    // 设置音频源
    elements.audioPlayer.src = url;
    console.log('✅ 音频源已设置');
    
    // 更新显示信息
    elements.currentSongTitle.textContent = title;
    elements.currentSongArtist.textContent = artist || '未知歌手';
    
    // 尝试加载音频
    elements.audioPlayer.load();
    console.log('📡 正在加载音频...');
    
    // 添加加载事件监听
    const onCanPlay = () => {
        console.log('✅ 音频加载成功，可以播放');
        elements.audioPlayer.removeEventListener('canplay', onCanPlay);
        elements.audioPlayer.removeEventListener('error', onError);
    };
    
    const onError = (e) => {
        console.error('❌ 音频加载失败:', e);
        console.error('  - 错误代码:', elements.audioPlayer.error?.code);
        console.error('  - 错误信息:', elements.audioPlayer.error?.message);
        showNotification('❌ 音频加载失败，请检查文件是否存在', 'error');
        elements.audioPlayer.removeEventListener('canplay', onCanPlay);
        elements.audioPlayer.removeEventListener('error', onError);
        isPlaying = false;
        updatePlayButton();
        elements.albumCover.classList.remove('playing');
    };
    
    elements.audioPlayer.addEventListener('canplay', onCanPlay, { once: true });
    elements.audioPlayer.addEventListener('error', onError, { once: true });
    
    // 尝试播放
    const playPromise = elements.audioPlayer.play();
    
    if (playPromise !== undefined) {
        playPromise.then(() => {
            console.log('✅ 播放成功');
            isPlaying = true;
            updatePlayButton();
            elements.albumCover.classList.add('playing');
        }).catch(err => {
            console.error('❌ 播放失败:', err);
            console.error('❌ 错误类型:', err.name);
            console.error('❌ 错误信息:', err.message);
            
            // 检查是否是自动播放被阻止
            if (err.name === 'NotAllowedError') {
                showNotification('⚠️ 浏览器阻止了自动播放，请点击播放按钮', 'info');
                console.log('👆 请用户手动点击播放按钮');
            } else {
                showNotification('❌ 播放失败: ' + err.message, 'error');
            }
            
            isPlaying = false;
            updatePlayButton();
            elements.albumCover.classList.remove('playing');
        });
    }
}

// ==================== 播放/暂停切换 ====================
function togglePlayPause() {
    if (!elements.audioPlayer.src) {
        showNotification('⚠️ 请先选择一首歌曲', 'info');
        return;
    }
    
    if (isPlaying) {
        elements.audioPlayer.pause();
        isPlaying = false;
        elements.albumCover.classList.remove('playing');
    } else {
        elements.audioPlayer.play();
        isPlaying = true;
        elements.albumCover.classList.add('playing');
    }
    
    updatePlayButton();
}

// ==================== 更新播放按钮 ====================
function updatePlayButton() {
    const icon = document.getElementById('playPauseIcon');
    if (!icon) return;
    icon.textContent = isPlaying ? '⏸️' : '▶️';
}

// ==================== 上一曲 ====================
async function playPrevious() {
    if (currentTrackIndex > 0) {
        const prevTrack = currentPlaylist[currentTrackIndex - 1];
        await playFromLibrary(currentTrackIndex - 1, prevTrack);
    } else {
        showNotification('⚠️ 已经是第一首了', 'info');
    }
}

// ==================== 下一曲 ====================
async function playNext() {
    console.log('🔄 playNext 被调用');
    console.log('  - 当前索引:', currentTrackIndex);
    console.log('  - 播放列表长度:', currentPlaylist.length);
    
    // 先清理当前临时文件
    if (currentTempFile) {
        console.log('🧹 清理当前临时文件:', currentTempFile);
        await cleanupTempFile(currentTempFile);
        currentTempFile = null;
    }
    
    if (currentTrackIndex < currentPlaylist.length - 1) {
        const nextTrack = currentPlaylist[currentTrackIndex + 1];
        console.log('▶️ 准备播放下一首:', nextTrack.title || nextTrack.name);
        await playFromLibrary(currentTrackIndex + 1, nextTrack);
    } else {
        console.log('⚠️ 已经是最后一首');
        showNotification('⚠️ 已经是最后一首了', 'info');
        elements.audioPlayer.pause();
        isPlaying = false;
        updatePlayButton();
        elements.albumCover.classList.remove('playing');
    }
}

// ==================== 清理临时文件 ====================
async function cleanupTempFile(filename) {
    if (!filename) return;
    
    try {
        console.log(`🧹 清理临时文件: ${filename}`);
        const response = await fetch(`/api/cleanup/${filename}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (data.success) {
            console.log(`✅ 临时文件已清理: ${filename}`);
        }
    } catch (error) {
        console.error('清理临时文件失败:', error);
    }
}

// ==================== 更新进度条 ====================
function updateProgress() {
    const current = elements.audioPlayer.currentTime;
    const duration = elements.audioPlayer.duration;
    
    if (duration) {
        const percent = (current / duration) * 100;
        updateProgressVisual(percent);
        elements.currentTime.textContent = formatTime(current);
    }
}

function updateProgressVisual(percent) {
    if (percent === undefined) {
        percent = (elements.audioPlayer.currentTime / elements.audioPlayer.duration) * 100 || 0;
    }
    elements.progressSlider.value = percent;
    elements.progressFill.style.width = percent + '%';
    if (elements.progressHandle) {
        elements.progressHandle.style.left = percent + '%';
    }
}

// ==================== 加载音乐库 ====================
async function loadLibrary() {
    try {
        const response = await fetch('/api/library');
        const data = await response.json();
        
        if (data.success) {
            displayLibrary(data.data);
        } else {
            console.error('加载失败:', data.message);
        }
    } catch (error) {
        console.error('加载音乐库错误:', error);
    }
}

// ==================== 显示音乐库 ====================
function displayLibrary(library) {
    elements.libraryList.innerHTML = '';
    
    if (library.length === 0) {
        elements.libraryEmpty.style.display = 'block';
        return;
    }
    
    elements.libraryEmpty.style.display = 'none';
    
    library.forEach((item, index) => {
        const musicItem = createMusicItem(item, index, 'library');
        elements.libraryList.appendChild(musicItem);
    });
    
    // 保存曲库播放列表
    currentPlaylist = library;
    
    // 为曲库播放按钮添加事件监听
    document.querySelectorAll('.play-from-library-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const index = parseInt(e.currentTarget.dataset.index);
            const item = currentPlaylist[index];
            await playFromLibrary(index, item);
        });
    });
}

// ==================== 下载当前歌曲 ====================
function downloadCurrentSong() {
    if (currentFilename) {
        downloadFile(currentFilename);
    } else {
        showNotification('⚠️ 当前没有正在播放的歌曲', 'info');
    }
}

// ==================== 下载文件 ====================
function downloadFile(filename) {
    const a = document.createElement('a');
    a.href = `/api/file/${filename}`;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    showNotification('💾 开始下载...', 'success');
}

// ==================== 删除音乐记录 ====================
async function deleteMusic(musicId) {
    if (!confirm('确定要删除这条音乐记录吗？')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/delete/${musicId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (data.success) {
            showNotification('✅ 删除成功', 'success');
            // 重新加载曲库
            loadLibrary();
        } else {
            showNotification(`❌ ${data.message}`, 'error');
        }
    } catch (error) {
        console.error('删除失败:', error);
        showNotification('❌ 删除失败', 'error');
    }
}

// ==================== 音频播放器初始化 ====================
function initAudioPlayer() {
    console.log('🎵 初始化音频播放器');
    
    // 检查播放器是否存在
    if (!elements.audioPlayer) {
        console.error('❌ 音频播放器元素未找到！');
        return;
    }
    
    console.log('✅ 音频播放器元素已找到');
    console.log('  - 音量:', elements.audioPlayer.volume);
    console.log('  - 静音:', elements.audioPlayer.muted);
    
    // 音频事件监听
    elements.audioPlayer.addEventListener('timeupdate', updateProgress);
    elements.audioPlayer.addEventListener('ended', playNext);
    
    elements.audioPlayer.addEventListener('loadedmetadata', () => {
        console.log('✅ 音频元数据已加载');
        console.log('  - 时长:', elements.audioPlayer.duration, '秒');
        elements.totalTime.textContent = formatTime(elements.audioPlayer.duration);
    });
    
    elements.audioPlayer.addEventListener('loadstart', () => {
        console.log('📡 开始加载音频...');
    });
    
    elements.audioPlayer.addEventListener('canplay', () => {
        console.log('✅ 音频可以播放');
    });
    
    elements.audioPlayer.addEventListener('playing', () => {
        console.log('▶️ 音频正在播放');
    });
    
    elements.audioPlayer.addEventListener('play', () => {
        console.log('▶️ play 事件触发');
        isPlaying = true;
        updatePlayButton();
        elements.albumCover.classList.add('playing');
    });
    
    elements.audioPlayer.addEventListener('pause', () => {
        console.log('⏸️ pause 事件触发');
        isPlaying = false;
        updatePlayButton();
        elements.albumCover.classList.remove('playing');
    });
    
    elements.audioPlayer.addEventListener('error', (e) => {
        console.error('❌ 音频错误事件:', e);
        if (elements.audioPlayer.error) {
            console.error('  - 错误代码:', elements.audioPlayer.error.code);
            console.error('  - 错误信息:', elements.audioPlayer.error.message);
            
            // 错误代码说明
            const errorMessages = {
                1: 'MEDIA_ERR_ABORTED - 播放被终止',
                2: 'MEDIA_ERR_NETWORK - 网络错误',
                3: 'MEDIA_ERR_DECODE - 解码错误',
                4: 'MEDIA_ERR_SRC_NOT_SUPPORTED - 不支持的格式'
            };
            console.error('  - 详情:', errorMessages[elements.audioPlayer.error.code] || '未知错误');
        }
    });
    
    elements.audioPlayer.addEventListener('stalled', () => {
        console.warn('⚠️ 音频加载停滞');
    });
    
    elements.audioPlayer.addEventListener('waiting', () => {
        console.log('⏳ 缓冲中...');
    });
    
    // 设置初始音量
    elements.audioPlayer.volume = 0.8;
    elements.audioPlayer.muted = false;
    console.log('✅ 音量设置为 0.8，静音: false');
    
    console.log('✅ 音频播放器初始化完成');
}

// ==================== 音量控制 ====================
function toggleMute() {
    if (elements.audioPlayer.volume > 0) {
        elements.audioPlayer.volume = 0;
        elements.volumeSlider.value = 0;
        updateVolumeIcon(0);
    } else {
        elements.audioPlayer.volume = 0.8;
        elements.volumeSlider.value = 80;
        updateVolumeIcon(80);
    }
}

function updateVolumeIcon(volume) {
    const icon = document.getElementById('volumeIcon');
    if (!icon) return;
    
    if (volume == 0) {
        icon.textContent = '🔇';
    } else if (volume < 50) {
        icon.textContent = '🔉';
    } else {
        icon.textContent = '🔊';
    }
}

// ==================== 工具函数 ====================
function formatTime(seconds) {
    if (isNaN(seconds) || !isFinite(seconds)) return '00:00';
    
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeAttr(text) {
    if (!text) return '';
    return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// ==================== 通知功能 ====================
function showNotification(message, type = 'info') {
    elements.notification.textContent = message;
    elements.notification.className = `notification ${type}`;
    elements.notification.classList.add('show');
    
    setTimeout(() => {
        elements.notification.classList.remove('show');
    }, 3000);
}

// ==================== 用户认证相关 ====================

// 检查用户登录状态
async function checkUserStatus() {
    try {
        const response = await fetch('/api/user/info');
        const data = await response.json();
        
        const authButtons = document.getElementById('authButtons');
        const userInfo = document.getElementById('userInfo');
        const userName = document.getElementById('userName');
        
        if (data.is_authenticated && data.data) {
            // 已登录
            authButtons.style.display = 'none';
            userInfo.style.display = 'flex';
            userName.textContent = data.data.username;
        } else {
            // 未登录
            authButtons.style.display = 'flex';
            userInfo.style.display = 'none';
        }
    } catch (error) {
        console.error('检查用户状态失败:', error);
    }
}

// 登出功能
document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            try {
                const response = await fetch('/api/logout', {
                    method: 'POST'
                });
                const data = await response.json();
                
                if (data.success) {
                    showNotification('✅ 已退出登录', 'success');
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 1000);
                } else {
                    showNotification('❌ 退出失败', 'error');
                }
            } catch (error) {
                console.error('退出失败:', error);
                showNotification('❌ 网络错误', 'error');
            }
        });
    }
});