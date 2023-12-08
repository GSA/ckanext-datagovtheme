async function getGeoplatformLink() {
    let parentEl = document.getElementById("geoplatform-link-section");
    if (parentEl == null) {
        return;
    }
    let datasetName = parentEl.getAttribute("data-package-name");
    try {
        const response = await fetch(
            `https://stg-api.geoplatform.gov/v3/public/lookups/data-gov/dataset?name=${datasetName}`
        )
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }
            })
            .then((data) => {
                let el = document.getElementById("geoplatform-link");
                el.href = data.geoplatform_url;
                parentEl.classList.remove("hide");
            });
    } catch (error) {
        console.error(error);
    }
}

getGeoplatformLink();
