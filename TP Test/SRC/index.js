const links = document.querySelectorAll("ul li")

icons.addEventListener("click", () => {
    nav.classList.toggle("active")
})

icons.addEventListener("click", () => {
    princ.classList.toggle("active")
})

icons.addEventListener("click", () => {
    log.classList.toggle("active")
})

links.forEach((link) => {
    link.addEventListener("click", () => {
        nav.classList.remove("active")
    })
})

links.forEach((link) => {
    link.addEventListener("click", () => {
        princ.classList.remove("active")
    })
})

links.forEach((link) => {
    link.addEventListener("click", () => {
        log.classList.remove("active")
    })
})