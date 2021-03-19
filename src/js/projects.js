let projects = 
[
    {
        name: "NoExcess",
        description: "My godawful, jank compiled programming language",
        date: new Date("2021-03-15"),
        path: "./content/projects/NoExcess/NoExcess.html",
        picture: "./content/projects/NoExcess/NoExcess.jpg",
    },
    {
        name: "PanTech website",
        description: "My godawful, jank website. First time making one so don't judge too hard.",
        date: new Date("2021-03-15"),
        path: "./content/projects/prestonpan/prestonpan.html",
        picture: null,
    },
    {
        name: "My dotfiles",
        date: new Date("2021-03-18"),
        description: "My minimal linux dotfiles (dwm + arch + dracula color theme), some stolen from distrotube though",
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