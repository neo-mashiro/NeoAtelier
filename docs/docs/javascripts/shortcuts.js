keyboard$.subscribe(function(key) {
    if (key.mode === "global" && key.type === "W") {
        window.scrollTo({top:0, left:0, behavior:'smooth'})
        key.claim()
    }
    else if (key.mode === "global" && key.type === "S") {
        window.scrollTo({top:document.body.scrollHeight, left:0, behavior:'smooth'})
        key.claim()
    }
})