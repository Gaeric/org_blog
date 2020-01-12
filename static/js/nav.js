window.addEventListener('scroll', function(e) {
  const height = ${'导航栏高度'};
  const scrollTop = document.documentElement.scrollTop; // 滚动条下移距离
  if (scrollTop >= height) {
    $(content-table).与顶部高度 = height;
  } else {
    $(content-table).与顶部高度 = height - scrollTop；
  }
});
