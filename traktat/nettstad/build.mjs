import {readFile, mkdir, cp, rm, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {validateEdition} from './content.mjs';

const root=path.dirname(fileURLToPath(import.meta.url));
const tractate=path.dirname(root);
const text=await readFile(path.join(tractate,'tekst/formlaere.txt'),'utf8');
const catalogText=await readFile(path.join(tractate,'kjelder.json'),'utf8');
const catalog=JSON.parse(catalogText);
const {props}=validateEdition(text,catalog);
const out=path.join(root,'dist');
await rm(out,{recursive:true,force:true});
await mkdir(path.join(out,'data'),{recursive:true});
await mkdir(path.join(out,'traktat'),{recursive:true});
for(const name of ['index.html','reader.js','reader.css','content.mjs','illustrations']){
  await cp(path.join(root,name),path.join(out,name),{recursive:true});
}
await writeFile(path.join(out,'data/formlaere.txt'),text);
await writeFile(path.join(out,'data/kjelder.json'),catalogText);
await cp(path.join(tractate,'pdf/traktat.pdf'),path.join(out,'traktat.pdf'));
// Keep existing bookmarked reader URLs working after moving to this repository.
await cp(path.join(root,'index.html'),path.join(out,'traktat/scroll.html'));
await cp(path.join(root,'index.html'),path.join(out,'traktat/index.html'));
console.log(`Bygde FORMLÆRE: ${props.length} proposisjonar, ${catalog.sources.length} kjelder.`);
