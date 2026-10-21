import * as si from 'simple-icons';
const want = {
 JavaScript:['siJavascript'],TypeScript:['siTypescript'],Python:['siPython'],HTML5:['siHtml5'],CSS3:['siCss3','siCss'],
 React:['siReact'],Next:['siNextdotjs'],Redux:['siRedux'],Zustand:['siZustand'],TanStack:['siReactquery','siTanstack'],Tailwind:['siTailwindcss'],
 Node:['siNodedotjs'],Express:['siExpress'],JWT:['siJsonwebtokens'],OAuth:['siAuth0'],Mongoose:['siMongoose'],Jest:['siJest'],
 PostgreSQL:['siPostgresql'],MySQL:['siMysql'],MongoDB:['siMongodb'],
 AWS:['siAmazonwebservices','siAmazonaws'],Docker:['siDocker'],Git:['siGit'],GitHub:['siGithub'],CICD:['siGithubactions'],
 Datadog:['siDatadog'],Postman:['siPostman'],PowerBI:['siPowerbi'],Jira:['siJira'],Figma:['siFigma'],
 LinkedIn:['siLinkedin'],X:['siX'],Instagram:['siInstagram'],Gmail:['siGmail']
};
const out={},missing=[];
for(const [k,names] of Object.entries(want)){
  const n=names.find(n=>si[n]);
  if(n) out[k]={path:si[n].path,hex:si[n].hex}; else missing.push(k);
}
import fs from 'fs'; fs.writeFileSync('icons.json',JSON.stringify(out));
console.log('found',Object.keys(out).length,'missing',missing.join(','));
