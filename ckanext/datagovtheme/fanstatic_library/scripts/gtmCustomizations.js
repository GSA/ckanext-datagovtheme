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
  const publisherObjIndex = window.dataLayer.findIndex((o) => o.id === 'datasetPublisher');
  const publisherObj = {
    id: 'datasetPublisher',
    event: 'new_view',
    agency: getPublisher(),
    dataSetName: document.querySelectorAll('h1[itemprop="name"]')[0]?.innerText || null,
    uri: window.location.pathname,
  };

  if (publisherObjIndex === -1) {
    window.dataLayer.push(publisherObj);
  } else {
    window.dataLayer[publisherObjIndex] = publisherObj;
  }
}
