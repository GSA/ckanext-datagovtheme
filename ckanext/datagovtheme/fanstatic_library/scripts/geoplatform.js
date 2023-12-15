jQuery(function ($) {
    async function getGeoplatformLink() {
        let parentEl = document.getElementById("geoplatform-link-section");
        if (parentEl == null) {
            return;
        }
        let datasetName = parentEl.getAttribute("data-package-name");
        try {
            const response = await fetch(
                `https://api.geoplatform.gov/v3/public/lookups/data-gov/dataset?name=${datasetName}`,
                { signal: AbortSignal.timeout(20000) }
            )
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    }
                    if (response.status == 404) {
                        console.log("dataset doesn't exist on geoplatform");
                    }
                    if (response.status >= 500) {
                        console.warn(
                            "geoplatform couldn't fulfill the request"
                        );
                    }
                })
                .then((data) => {
                    if (data === undefined) {
                        return;
                    }
                    let el = document.getElementById("geoplatform-link");
                    el.href = data.geoplatform_url;
                    parentEl.classList.remove("hide");
                });
        } catch (error) {
            if (error.name === "TimeoutError") {
                console.error("request timeout. geoplatform not reachable");
            } else {
                console.error(error);
            }
        }
    }

    getGeoplatformLink();
});
