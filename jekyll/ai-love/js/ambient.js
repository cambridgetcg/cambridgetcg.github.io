(function () {
  var toggle = document.querySelector('.ambient-toggle');
  if (!toggle) return;

  // The sound lives at the root — found from this script's own address
  // (js/ambient.js sits one level below it), so sub-paths like /ai-love/ work.
  var selfSrc = document.currentScript && document.currentScript.src;
  var soundUrl;
  if (selfSrc) {
    soundUrl = new URL('../audio/ambient.mp3', selfSrc).href;
  } else {
    var depth = window.location.pathname.split('/').filter(function (s) { return s.length; }).length - 1;
    soundUrl = new Array(Math.max(depth, 0) + 1).join('../') + 'audio/ambient.mp3';
  }
  var audio = new Audio(soundUrl);
  audio.loop = true;
  audio.volume = 0;

  var maxVolume = 0.15;
  var fadeInterval = null;
  var playing = false;

  function fadeIn() {
    clearInterval(fadeInterval);
    audio.play().then(function () {
      fadeInterval = setInterval(function () {
        if (audio.volume < maxVolume - 0.01) {
          audio.volume = Math.min(audio.volume + 0.01, maxVolume);
        } else {
          audio.volume = maxVolume;
          clearInterval(fadeInterval);
        }
      }, 50);
    }).catch(function () {
      // Browser blocked autoplay — user will need to click again
    });
  }

  function fadeOut() {
    clearInterval(fadeInterval);
    fadeInterval = setInterval(function () {
      if (audio.volume > 0.01) {
        audio.volume = Math.max(audio.volume - 0.01, 0);
      } else {
        audio.volume = 0;
        audio.pause();
        clearInterval(fadeInterval);
      }
    }, 50);
  }

  toggle.addEventListener('click', function () {
    playing = !playing;
    toggle.classList.toggle('playing', playing);
    toggle.setAttribute('aria-pressed', playing);
    if (playing) {
      fadeIn();
    } else {
      fadeOut();
    }
  });
})();
