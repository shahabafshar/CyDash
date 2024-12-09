document.addEventListener("DOMContentLoaded", function () {
    const contentDiv = document.getElementById("dashboard-content");

    // Fetch filter values on page load
    fetch("/get_filter_values")
        .then((response) => response.json())
        .then((data) => {
            populateDropdown("year-filter", data.years);
            populateDropdown("actor-type-filter", data.actor_types);
            populateDropdown("country-filter", data.countries);
        })
        .catch((err) => console.error("Error fetching filter values:", err));

    function populateDropdown(dropdownId, values) {
        const dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = ""; // Clear existing options
        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "All";
        dropdown.appendChild(defaultOption);

        values.forEach((value) => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value;
            dropdown.appendChild(option);
        });
    }

    // Load initial content (Overview tab)
    loadTabContent("overview");

    // Event listener for tabs
    document.querySelectorAll(".nav-link").forEach((tab) => {
        tab.addEventListener("click", (e) => {
            e.preventDefault();
            document.querySelectorAll(".nav-link").forEach((t) => t.classList.remove("active"));
            tab.classList.add("active");
            const selectedTab = tab.getAttribute("data-tab");
            loadTabContent(selectedTab);
        });
    });

    // Event listener for filters
    document.getElementById("apply-filters").addEventListener("click", () => {
        const year = document.getElementById("year-filter").value;
        const actorType = document.getElementById("actor-type-filter").value;
        const country = document.getElementById("country-filter").value;
        const activeTab = document.querySelector(".nav-link.active").getAttribute("data-tab");

        loadTabContent(activeTab, { year, actorType, country });
    });

    // Function to load tab content via AJAX
    function loadTabContent(tab, filters = {}) {
        const params = new URLSearchParams({ tab, ...filters }).toString();
        fetch(`/get_tab_content?${params}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then((html) => {
                contentDiv.innerHTML = html;
                const scripts = contentDiv.querySelectorAll("script");
                scripts.forEach((script) => {
                    const newScript = document.createElement("script");
                    newScript.textContent = script.textContent;
                    document.body.appendChild(newScript);
                    document.body.removeChild(newScript);
                });
            })
            .catch((err) => console.error("Error loading tab content:", err));
    }
});
