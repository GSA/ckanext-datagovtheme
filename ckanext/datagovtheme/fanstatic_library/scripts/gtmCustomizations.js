// Only execute this code on dataset pages
if (window.location.pathname.match(/^\/dataset\/.*$/g)) {
  const getPublisher = () => {
    const nodeList = document.querySelectorAll(`[property="dct:publisher"]`);
    if (nodeList.length === 1) {
      return nodeList[0]?.innerHTML.replaceAll(/<[^>]*>/gi, '').trim();
    }

    return 'err - multiple or no publisher';
  };

  const getOrgKeys = () => {
    const idNodeList = document.querySelectorAll('div[class="org_type"] a');
    const nameNodeList = document.querySelectorAll('div[class="org_type"] h1[class="heading"]');
    const keys = {
      organizationId: 'err - multiple or no organization',
      organizationName: 'err - multiple or no organization',
    };

    if (idNodeList.length === 1) {
      keys.organizationId = idNodeList[0]?.getAttribute('href').split('/organization/').pop();
    }

    if (nameNodeList.length === 1) {
      keys.organizationName = nameNodeList[0]?.innerHTML.trim();
    }

    return keys;
  };

  window.dataLayer = window.dataLayer || [];
  const publisherObjIndex = window.dataLayer.findIndex((o) => o.id === 'customDatasetKeys');
  const publisherObj = {
    id: 'customDatasetKeys',
    event: 'new_view',
    publisher: getPublisher(),
    ...getOrgKeys(),
    dataSetName: document.querySelectorAll('h1[itemprop="name"]')[0]?.innerText || null,
    uri: window.location.pathname,
  };

  if (publisherObjIndex === -1) {
    window.dataLayer.push(publisherObj);
  } else {
    window.dataLayer[publisherObjIndex] = publisherObj;
  }
}
