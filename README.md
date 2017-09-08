# SPOT Ontology Tooling Tutorial

This is a short interactive introduction to the SPOT Ontology Toolkit.

In this tutorial you will learn how to:
 
 * Install Solr
 * Index some example data
 * Use an example web application to search this data
 * Go through the SPOT ontology tools in order to annotate the example data
   * Zooma - a tool for automatic data annotation: www.ebi.ac.uk/spot/zooma
   * OLS - the Ontology Lookup Service: www.ebi.ac.uk/ols
   * OxO - the Ontology Xref Service: www.ebi.ac.uk/spot/oxo
   * Webulous - a tool for guided ontology development: www.ebi.ac.uk/efo/webulous
 * Install BioSolr - ontology expansion plugin for Solr, to exploit the annotated example data
 * Configure BioSolr
 * Perform ontology-powered searches

## Prerequisites

 * Java 8 - both Solr and the example web application rely on Java 8 to run.
 
## Part One - Installing Solr

Download Solr from http://lucene.apache.org/solr/ (Pick .tgz or .zip file as you prefer)

Unpack the Solr download into your preferred directory - for this demo, we're going to use `~/Applications/solr-5.3.1/`
    
Once you've done this, verify you can startup Solr:
```
>: cd ~/Applications/solr-5.3.1/
>: bin/solr start
```

Now open a browser and check we can see the Solr admin page at [http://localhost:8983/](http://localhost:8983/)

Now we're happy we can run Solr, so let's shut down our Solr server again...
```
>: bin/solr stop
```
...and now get the extra BioSolr stuff.  We'll be using this later in the tutorial

Check out the code for this demo into your preferred directory - we're going to be using `~/Projects/`:
```
>: cd ~/Projects
>: git clone https://github.com/EBISPOT/ICBO2017.git
```

We've supplied the required configuration to get us up and running quickly, so let's start a new Solr instance that uses this config:
```
>: cd ~/Projects/ICBO2017/solr
>: export SOLR_DIR=~/Applications/solr-5.3.1
>: solr-start.sh
```

Now reload your page at [http://localhost:8983/](http://localhost:8983/) - this time, you should see a new documents core.  If so, great! Now we're ready to start indexing some data.

## Part Two - Indexing some example data

We've supplied some sample data that we will be annotating to ontology terms. This data is stored in the file `data/gwas-catalog-data-lung.csv` - you can open this file in Excel and take a look at it if you like.
It contains information for GWAS studies. The study titles, pubmed id's are provided, along with the trait that is identified with each study.

All the studies are associated with the lung and lung diseases.

Our goal will be to eventually annotate all the study traits with ontology terms. 

But let's try and index the information we already have and search through it.

*For reference:*
**Data** is taken from the GWAS Catalog: http://www.ebi.ac.uk/gwas

Now let's index this data.  You can upload CSV files directly to Solr using curl:

```
>: curl http://localhost:8983/solr/documents/update --data-binary @../data/gwas-catalog-data-lung.csv -H 'Content-type:application/csv'
>: curl http://localhost:8983/solr/documents/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
```

The first command here uploads the data, the second one commits the changes and makes your newly indexed documents visible.

Now, if you open the admin interface once more and look at the overview of the documents core [http://localhost:8983/solr/#/documents](http://localhost:8983/solr/#/documents), you should see we now have 99 documents in our index.

We can also inspect some of the data by browsing to the query page [http://localhost:8983/solr/#/documents/query](http://localhost:8983/solr/#/documents/query) and running a standard query - you can see that the documents in our index correspond to rows in our spreadsheet.

## Part Three - Run the sample web application

Next, we've supplied you with a simple web application to search our new Solr index.  Let's try running this.

```
>: cd ~/Projects/ICBO2017/tools
>: java -jar webapp-1.0-SNAPSHOT.jar server webapp.yml
```

You should see a bunch of logging information as the web application starts up. If all goes well, you'll eventually see a message like this:
```
INFO  [2015-12-06 18:50:49,002] org.eclipse.jetty.server.Server: Started @1637ms
```

Now we can open up our example application by browsing to [http://localhost:8080/](http://localhost:8080/).

Let's try some example searches.  Most of the GWAS data is concerned with the links between SNPs and diseases - so let's try a search for `Lung cancer`.
Looks like we get 16 results, all containing lung cancer in the title or the association line, so for example:

> 1.    **Deciphering the impact of common genetic variation on lung cancer risk: a genome-wide association study.**  
>       Broderick P - Cancer Res.  
>       *rs8034191* is associated with *Lung cancer*  

But what if we want all lung diseases? We could try searching for `lung disease` - but this only gives us 2 results, probably not what we want.  We can try just searching for `lung`, which looks a little better - 25 results this time, some of them are lung cancer but there's also stuff about lung function, so this isn't ideal either.


#### Additional Tasks

- [x] Try searching for 'pulmonary' or 'pulmonary disease'. Given that pulmonary is a synonym for lung, would you want to have the option to see these reuslts under lung disease and vice versa?
- [x] What happens when you search for 'Boeck sarcoid'?
- [x] What happens when you search for 'respiratory system disease'?
- [x] If you select the checkboxes to include synonym, parent, child labels, does anything change?


## Part Four - Selecting our ontology(s)

It is now time we try and annotate our data to an ontology. 

Let's go look at our ontology options in the [Ontology Lookup Service (OLS)](www.ebi.ac.uk/ols).

The GWAS Catalog annotates it's traits to the [Experimental Factor Ontology (EFO)](www.ebi.ac.uk/efo) and that's what we will try to do to. 
-[x] Try and find EFO in OLS. 
-[x] Take a look at it's structure.
-[x] Find the 'Ontology history' tab and take a look at how EFO evolves over time. Active development of an ontology is a good indicator that this ontology is kept up to date. As the domain of biomedicine changes,
it is only natural that the ontologies representing that domain should reflect the changes.

Now that we have decided which ontology we will use, let's go an meet Zooma!

## Part Five - Automatic data annotation through Zooma 

Go to the data file and open the traits.tsv file (you can use your favorite editor to do this, or simply open the file up in excel).

```
 >: cd ~/Projects/ICBO2017/data
 >: vi traits.tsv
```

We have created a list of all of our study traits that need to be annotated to EFO. In this case we only have 22 traits to map. 
One option we have is to manually search for each term in OLS and keep the annotation that we want. But you usually will have a lot more data and need a process that is a bit more automated.

Go to the Zooma web page: www.ebi.ac.uk/spot/zooma

Copy the traits from the traits.tsv file into the text box and press the 'Annotate button'. Take a look at the results. 

A lot of teams at the EBI annotate their data with ontology terms. Because they don't want to do this all the time, they create data sources to store the mappings between their text data and ontology term. So next time they want to annotate the same terms, they don't need to look them up again. That's what Zooma does. It has a bunch of curated data sources from various teams at the EBI. When a text term is given to Zooma, Zooma will look to see if it has seen a suitable mapping for that term before before and will return the
mapping with a level of confidence. If Zooma hasn't seen the term before in it's data sources, it will go to OLS and try to find a good mapping there.

You can see the data sources that Zooma has, and customize your search as you want it. Click on 'Configure Datasources' and have a look around.

Most of our results we got should have the GWAS Catalog in the 'Source' column, and should have a HIGH Mapping confidence. This is expected, as we are looking at studies with traits that have already been annotated.

We will try and follow the curation steps for these studies to fit the GWAS Catalog standard. 

## Part Six - Zooma HIGH confidence

Select all the data sources, except GWAS, and run the annotation again. The results should not be as good this time. That's OK, we will make them better!

First let's look at the results that have a HIGH confidence. If you the sources that you have selected represent the domain of your data, you can use the mappings that have a high confidence withought looking at them again. 

We will copy these mappings to our traits.tsv file. Open traits-1.tsv in excel. We have already copied the high mappings into this file. Select the traits that don't have a mapping and lets go run them through Zooma again.

## Part Seven - Zooma GOOD confidence

For the results that didn't get a high mapping, let's run the same query (selecting all data sources, except GWAS). We can see that we have some resutls from some other data sources, that don't match very well, and some ontology matches. Zooma went and looked up our terms in OLS. Filter out the data sources in total (select 'Don't search in any datasources' in the 'Configure datasources' drop down window) and hit 'Annotate' again. The results look a little better for some terms.

We will focus on the mappings that have a good confidence and see if we like them and how we can improve them. We have done a bit of pre-processing to help you curate the good terms and ignore the medium mappings for now. 
Open the traits-2.tsv file in excel and filter the GOOD results. Select them and paste them into the Zooma box. Run the annotation (remember, we have chosen to exclude all data sources and let Zooma fall back to searching OLS for now). 

All the mappings should be of GOOD confidence. This means that Zooma found an exact label (or synonym) match for our terms in OLS. 

We want to map our terms to EFO. Some already mapped to EFO and that's great! We still need to look at them though to make sure that we are satisfied with the mapping, or that we don't need to alter our search to include more terms. 

For example `Age at smoking initiation in chronic obstructive pulmonary disease` mapped to `EFO_0000341` with label `chronic obstructive pulmonary disease`. We want to keep that mapping, but there is room for another one to be included. If we go to (OLS)[www.ebi.ac.uk/ols] and search for `smoking initiation` we get the EFO term `EFO_0005670`. So in this case we can have 2 mappings. 

Do the same for the other terms mapped to EFO. 


## Part Eight - Introducing OxO 

But what about the ones that mapped to a different ontology? Well let's throw them into OxO and see what we get!

Head over to (OxO)[www.ebi.ac.uk/spot/oxo]. OxO is a tool that helps you explore ontology-to-ontology cross references (or ontology-to-vocabulary cross references). So if the term `liver` exists in multiple ontologies, we can find all the common references to that term.

Copy and paste all the 'Ontology Class ID's of the other-than-efo-mapped-terms into OxO and select 'Find mappings. We can explore the links from each ontlogy class to an EFO ontology class, if it exists. 

Let's try clicking on NCIt:C2975 (Cystic Fibrosis). There is a link to EFO! If we select it and then click on 'View in OLS', we will be redirected to the term in OLS. We can see that the specific Xref leads to an obsolete efo class, but efo tells us what to use instead. 

You can do the same for the rest of the OxO Xref mappings, if there are any. For the ones that don't match, we will leave them blank.

## Part Nine - Restricting Zooma to an ontology

Term by term, we have curated the GOOD confidence results. Open the trait-2-curated.tsv file to see the terms after they have been curated. 

Again, let's select the un-mapped terms and go to Zooma. Open the trait-3.tsv file and select the ones with GOOD confidence. These are the ones that were left un-mapped after the last step. Copy them again into Zooma and customize the search.

We will exclude all data sources from our search, but now we will also go to 'Configure Ontology Sources' and select only EFO!

Almost all of our mappings are GOOD. We will go though the same process as in step seven and curate any terms that might need curation. 
The result of the curation is in the traits-3-curated.tsv file. Almost done, only one term left!

## Part Ten - Creating a new ontology class through Webulous

We can see the one term is left without a mapping to an EFO class: `Pneumoconiosis in silica exposure`

If we search for the term in OLS we will be able to find a suitable match for it. But let's pretend that there isn't one. This will sometimes happen with your data. Sometimes your data isn't represented yet in the ontology you want - or in any ontology! 

We will see how to create a new class in an ontology using (Webulous)[www.ebi.ac.uk/efo/webilous]. 

Webulous is a tool for guided ontology development. You can specify ontology design patterns in Webulous and populate them with data. There is a built in ontology searcher and validator. 

## Part Eleven - Install BioSolr plugins

We have our data all annotated. Now we're going to try and improve our search results using the structure of the ontology.  To do this, we need to add the BioSolr ontology expansion plugin.

Before we start, let's shutdown our running Solr server

```
>: cd ~/Projects/ICBO2017/solr/
>: solr_stop.sh
```

Now, take the BioSolr plugin jar file out of the `plugins/` directory and copy it into our Solr setup.

```
>: mkdir solr-conf/documents/lib
>: cp ../plugins/solr-ontology-update-processor-0.5.jar solr-conf/documents/lib/
```

We've installed our plugin, but we need to do a bit of reconfiguration to make Solr use it.


## Part Twelve - Configure BioSolr

Now we need to modify our Solr configuration to make use of this plugin.

### Adding an Ontology Lookup Processor Chain

We need to add our plugin - an OntologyUpdateProcessor - to our default processor chain in Solr, so that Solr will perform the ontology lookup from our configured field.

You'll need to edit `solr-conf/documents/conf/solrconfig.xml`.  Scroll down to line 619 and uncomment this block:

```
  <!-- Ontology lookup processor chain -->

  <updateRequestProcessorChain name="ontology">
    <processor class="uk.co.flax.biosolr.solr.update.processor.OntologyUpdateProcessorFactory">
      <bool name="enabled">true</bool>
      <str name="annotationField">efo_uri</str>

      <str name="olsBaseURL">http://www.ebi.ac.uk/ols/api</str>
      <str name="olsOntology">efo</str>
    </processor>
    <processor class="solr.LogUpdateProcessorFactory" />
    <processor class="solr.DistributedUpdateProcessorFactory" />
    <processor class="solr.RunUpdateProcessorFactory" />
  </updateRequestProcessorChain>
```

Let's take a look at this in a bit of detail.  We're setting up a processor chain called 'ontology' that uses the class `OntologyUpdateProcessorFactory` that has been developed as part of BioSolr.  We've told it to look for annotation in the 'efo_uri' field, and told it where the Ontology Lookup Service (OLS) is located.  We've also told it to use the ontology 'efo' from OLS.

Now, we need to add this update request processor chain to our update request handler, so it is used whenever we update data.

Still editing `solr-conf/documents/conf/solrconfig.xml`, scroll back up to line 431 and uncomment this block:

```
  <requestHandler name="/update" class="solr.UpdateRequestHandler">
    <!-- See below for information on defining
         updateRequestProcessorChains that can be used by name
         on each Update Request
      -->
       <lst name="defaults">
         <str name="update.chain">ontology</str>
       </lst>
  </requestHandler>
```

Now we've reconfigured our server, we just have to restart...
```
>: cd ~/Projects/ICBO2017/solr/
>: solr-start.sh
```

## Part Thirteen - Reindex our data to take advantage of ontology enrichment

This bit is simple - we can just rerun our indexing process from earlier...

```
>: curl http://localhost:8983/solr/documents/update --data-binary @../data/gwas-catalog-data-lung.csv -H 'Content-type:application/csv'
>: curl http://localhost:8983/solr/documents/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
```

You'll notice this takes a while longer than it did earlier - this is because this time, as we index our data we're calling out to OLS to expand our data using the ontology.  Hopefully network access is up to it!

If you open the Solr admin interface again [http://localhost:8983/solr/#/documents](http://localhost:8983/solr/#/documents), we should still have 99 documents.  But if we do a query - http://localhost:8983/solr/#/documents/query - you should see a lot more information than we had earlier, including some new fields that weren't in our spreadsheet.

## Part Fourteen - Ontology-powered search!

Now let's go back to our web application and see if we can take advantage of all this extra information.

Restart the application again:
```
>: cd ~/Projects/ICBO2017/tools
>: java -jar webapp-1.0-SNAPSHOT.jar server webapp.yml
```
You'll straight away notice something new - some additional checkboxes (you might need to reload your page).  These are present because our webapp has noticed that we have additional ontology fields in our data.

Now let's go back to our earlier searches.  If you remember, we tried looking for `lung cancer` and we got 16 results.  We should be able to do the same search again, and get the same results.

Then, we tried `lung disease` and only got 3 results.  Again, we should be able to verify this. But now let's check the box to use ontology expansion:
- [x] Include parent labels
Now if we rerun the search, we should see 31 results, across a whole variety of lung disease.  One of our hits, for example, should look like this:

> 14.    **A genome-wide association study in chronic obstructive pulmonary disease (COPD): identification of two major susceptibility loci.**  
>       CPillai SG - PLoS Genet.  
>       *rs1828591* is associated with *Chronic obstructive pulmonary disease.*   
>       **Annotation** chronic obstructive pulmonary disease [http://www.ebi.ac.uk/efo/EFO_0000341].  
>       **Children** chronic bronchitis.  
>       **Parent(s)** lung disease.  
>       **Has disease location** trachea lung.  

This looks much more like it! But we can even go one better than this - let's try searching for `lung` again. Uncheck all the boxes so we get 25 results.
This time, though, let's also include diseases which are located in the lung...
- [x] "Has disease location"
Now you should see that we have 40 results; we're using relationships in the ontology to improve our results.  For example, one of our results looks like this:

> 26.   **A genome-wide association study identifies susceptibility loci of silica related pneumoconiosis in Han Chinese.
**  
>       Chu M - Hum Mol Genet.  
>       *rs73329476* is associated with *Pneumoconiosis in silica exposure.*  
>       **Annotation** pneumoconiosis [http://www.orpha.net/ORDO/Orphanet_182098].  
>       **Parent(s)** lung disease bacterial disease 
>       **Has disease location** lung

If you look closely, you'll see that "lung" is not mentioned anywhere in our data, only the extra fields that have come from the ontology.  We'd actually have picked this result up by including parents (`lung disease`), but this is only because EFO nicely defines hierarchy.  If we were using a different ontology with a different hierarchy (maybe one which doesn't use hierarchy in the ways we'd like), we can use a relationship other than `is a` to find this result.

This shows the power of including additional information from the ontology in your Solr index. You'll also see the search is just as fast as it was previously: by including extra data when we built our index, we have almost no penalty in search time - which is usually the best option for users.

#### Additional Tasks

- [x] Try searching for 'pulmonary' or 'pulmonary disease'. Given that pulmonary is a synonym for lung, would you want to have the option to see these reuslts under lung disease and vice versa?
- [x] What happens when you search for 'Boeck sarcoid'?
- [x] What happens when you search for 'respiratory system disease'?
- [x] If you select the checkboxes to include synonym, parent, child labels, does anything change?

## Conclusions

This is the end of the SPOT Ontology Tooling tutorial. You've seen how to install Solr, load some example data, go through a set of steps and tools to annotate your data to ontology, extend Solr with the ontology expansion plugin developed by BioSolr into a Solr installation, and you've seen some of the extra features this plugin can give you.

You can find a similar tutorial exclusively for BioSolr, along with the code for the webapp and the plugin, here - https://github.com/EBISPOT/BioSolr


*You can also do all of this using elasticsearch, not only Solr!*

For more about the team of SPOT and our tools around ontologies, head here - http://www.ebi.ac.uk/spot/ontology/



