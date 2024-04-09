// Only execute this code on dataset pages
if (window.location.pathname.match(/^\/dataset\/.*$/g)) {
  const getPublisher = () => {
    const nodeList = document.querySelectorAll(`[property="dct:publisher"]`);
    if (nodeList.length === 1) {
      return nodeList[0]?.innerHTML.replaceAll(/<[^>]*>/gi, '');
    }

    // fall through that we may not need
    return 'err - multiple or no publishers';
  };

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'new_view',
    agency: getPublisher(),
  });
}
