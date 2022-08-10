buttons = document.querySelector("[data-qa='wstrade-activity-list-past']").querySelectorAll("button")
out = {}
wait = (delay) => new Promise((res) => setTimeout(() => res(), delay))
for(let i = 0; i < buttons.length; i++) {
    let name = buttons[i].querySelector(".sc-ihNHHr.jjDDSu")
    if (!name) continue
    buttons[i].click()
    await wait(500)
    console.log(`Parsing ${name.innerText}`)
    if(!out[name.innerText]) out[name.innerText]=[]
    out[name.innerText].push(buttons[i].parentElement.innerHTML)
    buttons[i].click()
}

console.log("Done")
console.log(out)