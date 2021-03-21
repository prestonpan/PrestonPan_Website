// TODO: set up actual database. Only worth it when 15+ projects.
let projects = 
[
    {
        name: "NoExcess",
        description: "An elegant, and frankly useless compiled programming language.",
        date: new Date("2021-03-15"),
        path: "./content/projects/NoExcess/NoExcess.html",
        picture: "./content/projects/NoExcess/NoExcess.jpg",
    },
    {
        name: "PanTech website",
        description: "My godawful, jank website. Dracula themed so your eyes don't die.",
        date: new Date("2021-03-15"),
        path: "./content/projects/prestonpan/prestonpan.html",
        picture: null,
    },
    {
        name: "My dotfiles",
        date: new Date("2021-03-18"),
        description: "My minimal linux dotfiles (dwm + arch + dracula color theme), my distrobution of distrotube's distrobution of dwm",
        path: "./content/projects/my_dotfiles/my_dotfiles.html",
        picture: "./content/projects/my_dotfiles/my_dotfiles.png",
    },
];

const sorted_projects = projects.slice().sort((a, b) => b.date - a.date);
let final_html_projects = "";
if (document.title == "PanTech" && projects.length >= 3) {
    for(let j = 0; j < 3; j ++) {
        let a = sorted_projects[j]
        if (a.picture == null){
            final_html_projects += `<section><a href="${a.path}"><h3>${a.name}</h3></a><p>${a.description}</p></section>`
        } else {
            final_html_projects += `<a href="${a.path}"><h3>${a.name}</h3></a><section><figure><a href="${a.path}"><img src="${a.picture}"></a><figcaption>${a.description}</figcaption></figure></section>`
        }
    };
} else {
    for(let j = 0; j < projects.length; j ++) {
        let a = sorted_projects[j]
        if (a.picture == null){
            final_html_projects += `<section><a href="${a.path}"><h2>${a.name}</h2></a><p>${a.description}</p></section>`
        } else {
            final_html_projects += `<section><a href="${a.path}"><h2>${a.name}</h2></a><figure><a href="${a.path}"><img src="${a.picture}" alt=""></a><figcaption>${a.description}</figcaption></figure></section>`
        }
    };
}

const project = document.getElementById("projects")
project.innerHTML = final_html_projects