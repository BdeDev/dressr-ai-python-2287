/* ==============================================
   GET SCRIPT TAG ATTRIBUTES
============================================== */
var scriptTag = document.currentScript;
var calender_initial_date = scriptTag.dataset.calender_initial_date;
var user_id = scriptTag.dataset.user_id;
var calender_url = scriptTag.dataset.calender_url;

/* ==============================================
   DATE FUNCTION
============================================== */
Date.prototype.addDays = function (days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
};

/* ==============================================
   FULLCALENDAR INITIALIZATION
============================================== */
var calendarEl = document.getElementById("calendar");
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    editable: false,
    droppable: false,
    selectable: true,
    navLinks: false,
    events: [],
    eventOrder: "start",
    initialDate: calender_initial_date,
    dayMaxEventRows: true,

    views: {
        timeGrid: {
            dayMaxEventRows: 6,
        },
    },

    headerToolbar: {
        right: "prev,next today",
        center: "title",
        left: "",
    },

    /* =============================
       DATE SELECT
    ============================== */
    select: function (selectionInfo) {
        let selected_date = selectionInfo.start;
        console.log(selected_date, "selected date");
    },

    /* =============================
       FORMAT EVENT CONTENT
    ============================== */
    eventContent: function (arg) {
        return {
            html: arg.event.title,
        };
    },

    /* =============================
       LOAD DATA WHEN MONTH CHANGES
    ============================== */
    datesSet: function (dateInfo) {
        let current_date = dateInfo.start;
        current_date = current_date.addDays(10);

        $.ajax({
            url: calender_url,
            type: "GET",
            data: {
                user_id: user_id,
                month: current_date.getMonth() + 1,
                year: current_date.getFullYear(),
            },
            async: false,
            success: function (data) {
                calendar.removeAllEvents();

                let items_data = data.items_data;
                let mergedEvents = {};

                // GROUP ITEMS BY DATE
                items_data.forEach(function (item) {
                    let date = moment.utc(item.worn_on).local().format("YYYY-MM-DD");

                    if (!mergedEvents[date]) {
                        mergedEvents[date] = [];
                    }

                    mergedEvents[date].push({
                        id: item.id,
                        image: window.location.origin + "/media/" + item.item__image,
                    });
                });

                // ADD EVENTS TO CALENDAR
                Object.keys(mergedEvents).forEach(function (date) {
                    calendar.addEvent({
                        id: mergedEvents[date][0].id,
                        start: date,
                        extendedProps: {
                            images: mergedEvents[date],
                        },
                    });
                });
            },
        });
    },

    /* =============================
       SHOW IMAGE + "+ MORE" IN CELL
    ============================== */
    eventDidMount: function (info) {
        let images = info.event.extendedProps.images;

        if (!images || images.length === 0) return;

        info.el.innerHTML = "";

        let wrapper = document.createElement("div");
        wrapper.style.display = "flex";
        wrapper.style.flexDirection = "column";
        wrapper.style.alignItems = "center";

        // First image preview
        let img = document.createElement("img");
        img.src = images[0].image;
        img.style.width = "140px";
        img.style.height = "110px";
        img.style.objectFit = "cover";
        img.style.borderRadius = "6px";
        wrapper.appendChild(img);

        // + More Text
        if (images.length > 1) {
            let moreText = document.createElement("div");
            moreText.innerText = `+${images.length - 1} more`;
            moreText.style.marginTop = "4px";
            moreText.style.fontSize = "13px";
            moreText.style.fontWeight = "600";
            moreText.style.color = "#333";
            moreText.style.cursor = "pointer";

            // Attach click handler
            moreText.classList.add("open-gallery");
            moreText.dataset.images = JSON.stringify(images);

            wrapper.appendChild(moreText);
        }

        info.el.appendChild(wrapper);
    },
});

calendar.render();

/* ============================================================
   IMAGE GALLERY MODAL + SWIPER  (FULL WORKING)
============================================================ */

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("open-gallery")) {
        const images = JSON.parse(e.target.dataset.images);
        openImageGallery(images);
    }
});

/* --------------------------------------------------
   OPEN GALLERY
-------------------------------------------------- */
function openImageGallery(images) {
    const wrapper = document.getElementById("gallerySwiperWrapper");
    wrapper.innerHTML = "";

    images.forEach((img) => {
        wrapper.innerHTML += `
            <div class="swiper-slide">
                <img src="${img.image}" class="img-fluid w-100" style="height:350px;object-fit:cover;">
            </div>
        `;
    });

    // Show modal
    const modal = new bootstrap.Modal(
        document.getElementById("imageGalleryModal")
    );
    modal.show();

    setTimeout(() => initGallerySwiper(), 150);
}

/* --------------------------------------------------
   INIT SWIPER (DESTROY IF ALREADY EXISTS)
-------------------------------------------------- */
let gallerySwiper = null;

function initGallerySwiper() {
    if (gallerySwiper) {
        gallerySwiper.destroy(true, true);
    }

    gallerySwiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        centeredSlides: true,
        spaceBetween: 10,
        loop: true,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
        },
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
    });
}
