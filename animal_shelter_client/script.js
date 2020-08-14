async function go() {
    let r =await axios.post('https://8080-ec5b635c-512a-4ec2-a277-4d00344e1898.ws-us02.gitpod.io/api/animals', {
        "name": "Grey",
        "age": 4,
        "breed": "Tabby",
        "type": "5f34e6a8effcc3281952b667"
    })
    console.log(r)
}

go();