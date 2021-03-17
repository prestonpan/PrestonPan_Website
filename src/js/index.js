// WARNING: do not use spaces for the name field.
let projects = [{
        name: "NoExcess",
        description: "My godawful, jank compiled programming language",
        date: new Date("2021-03-15"),
    },
    {
        name: "PanTech website",
        description: "My godawful, jank website",
        date: new Date("2021-03-15"),
    },
    {
        name: "My dotfiles",
        date: new Date("2021-03-15"),
        description: "My minimal linux dotfiles (dwm + arch)",
    }
];

for (let i = 0; i < projects.length; i++) {
    projects[i].html_file = `.. /content/projects/${projects[i].name}/${projects[i].name}.html`
};

let sorted_dates = projects.slice().sort((a, b) => b.date - a.date);