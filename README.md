# SPOT Ontology Tooling Tutorial

This is a short interactive introduction to the SPOT Ontology Toolkit. the BioSolr Ontology Expansion plugin for Solr.

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

But what if we want all lung diseases? We could try searching for `lung disease` - but this only gives us 2 results, probably not what we want.  We can try just searching for `lung`, which looks a little better - 24 results this time, some of them are lung cancer but there's also stuff about lung function, so this isn't ideal either.


#### Additional Tasks

- [x] Try searching for 'pulmonary' or 'pulmonary disease'. Given that pulmonary is a synonym for lung, would you want to have the option to see these reuslts under lung disease and vice versa?
- [x] What happens when you search for 'Boeck sarcoid'?
- [x] What happens when you search for 'respiratory system disease'?
- [x] If you select the checkboxes to include synonym, parent, child labels, does anything change?


## Part Four - Selecting our ontology(s)

Now we are going to try and annotate our data to an ontology. 

Let's go look at our ontology options in the [Ontology Lookup Service (OLS)](www.ebi.ac.uk/ols).

The GWAS Catalog annotates it's traits to the [Experimental Factor Ontology (EFO)](www.ebi.ac.uk/efo) and that's what we will try to do to. Try and find EFO in OLS. Take a look at it's structure.
Find the 'Ontology history' tab and take a look at how EFO evolves over time. Active development of an ontology is a good indicator that this ontology is kept up to date. As the domain of biomedicine changes,
it is only natural that the ontologies representing that domain should reflect the changes.

Now that we have decided which ontology we will use, let's try and actually annotate our data to that ontoloy!

## Part Five - Automatic data annotation through Zooma 

Go to the data file and open the traits.tsv file (you can use your favorite editor to do this, or simply open the file up in excel).

```
 >: cd ~/Projects/ICBO2017/data
 >: vi traits.tsv
```

We have created a list of all of our study traits that need to be annotated to EFO. One option we have is to manually search for each term in OLS and keep the annotation that we want. 

Another option that we have is to use Zooma to try and do this semi-automatically.

Go to the Zooma web page: www.ebi.ac.uk/spot/zooma

Copy the traits from the traits.tsv file into the text box and press the 'Annotate button'. Take a look at the results. 

A lot of teams at the EBI annotate their data with ontology terms. Because they don't want to do this all the time, they create data sources to store the mappings between their text data and ontology term. So next time they want to annotate the same terms, they don't need to look them up again. That's what Zooma does. It has a bunch of curated data sources from various teams at the EBI. When a term is given to Zooma, Zooma will look to see if it has seen the term before and will return the
mapping with a level of confidence. If Zooma hasn't seen the term before in it's data sources, it will go to OLS and try to find a good mapping there.

You can see the data sources that Zooma has, and customize your search as you want it. Click on 'Configure Datasources' and have a look around.

Most of our results should have the GWAS Catalog in the 'Source' column, and should have a HIGH Mapping confidence. This is expected, as we are looking at studies with traits that have already been curated.

We will try and follow the curation steps for these studies to fit the GWAS Catalog standard. 

## Part six - Zooma HIGH results

Select all the datasources except GWAS, and run the annotation again. The results should not be as good this time. That's OK, we will make them better!

First let's look at the results that have a HIGH confidence. If you trust the sources that you have selected, you can use the mappings that have a high confidence withought looking at them again. It is unlikely that there will be a mis-match here. 



## Part Four - Install BioSolr plugins

Now we're going to try and improve our search results using the structure of the ontology.  To do this, we need to add the BioSolr ontology expansion plugin.

Before we start, let's shutdown our running Solr server

```
>: cd ~/Projects/BioSolr/tutorial/solr/
>: solr_stop.sh
```

Now, take the BioSolr plugin jar file out of the `plugins/` directory and copy it into our Solr setup.

```
>: mkdir solr-conf/documents/lib
>: cp ../plugins/solr-ontology-update-processor-0.5.jar solr-conf/documents/lib/
```

You can find the code of this plugin under the `BioSolr/ontology/ontology-annotator` directory.

We've installed our plugin, but we need to do a bit of reconfiguration to make Solr use it.


## Part Five - Configure BioSolr

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
>: cd ~/Projects/BioSolr/tutorial/solr/
>: solr-start.sh
```

## Part Six - Reindex our data to take advantage of ontology enrichment

This bit is simple - we can just rerun our indexing process from earlier...

```
>: curl http://localhost:8983/solr/documents/update --data-binary @../data/gwas-catalog-annotation-data.csv -H 'Content-type:application/csv'
>: curl http://localhost:8983/solr/documents/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
```

You'll notice this takes a while longer than it did earlier - this is because this time, as we index our data we're calling out to OLS to expand our data using the ontology.  Hopefully network access is up to it!

If you open the Solr admin interface again [http://localhost:8983/solr/#/documents](http://localhost:8983/solr/#/documents), we should still have 26,385 documents.  But if we do a query - http://localhost:8983/solr/#/documents/query - you should see a lot more information than we had earlier, including some new fields that weren't in our spreadsheet.

## Part Seven - Ontology-powered search!

Now let's go back to our web application and see if we can take advantage of all this extra information.

Restart the application again:
```
>: cd ~/Projects/BioSolr/tutorial/tools
>: java -jar webapp-1.0-SNAPSHOT.jar server webapp.yml
```
You'll straight away notice something new - lots of additional checkboxes (you might need to reload your page).  These are present because our webapp has noticed that we have additional ontology fields in our data.

Now let's go back to our earlier searches.  If you remember, we tried looking for `lung cancer` and we got 31 results.  We should be able to do the same search again, and get the same results.

Then, we tried `lung disease` and only got 3 results.  Again, we should be able to verify this. But now let's check the box to use ontology expansion:
- [x] Include parent labels
Now if we rerun the search, we should see 53 results, across a whole variety of lung disease.  One of our hits, for example, should look like this:

> 1.    **Variants in FAM13A are associated with chronic obstructive pulmonary disease.**  
>       Cho MH - Nat Genet.  
>       *rs7671167* is associated with *Chronic obstructive pulmonary disease.*   
>       **Annotation** chronic obstructive pulmonary disease [http://www.ebi.ac.uk/efo/EFO_0000341].  
>       **Children** chronic bronchitis.  
>       **Parent(s)** lung disease.  
>       **Has disease location** trachea lung.  

This looks much more like it! But we can even go one better than this - let's try searching for `lung` again. Uncheck all the boxes so we get 49 results.
This time, though, let's also include diseases which are located in the lung...
- [x] "Has disease location"
Now you should see that we have 75 results; we're using relationships in the ontology to improve our results.  For example, one of our results looks like this:

> 10.   **Genome-wide association study identifies BICD1 as a susceptibility gene for emphysema.**  
>       Kong X - Am J Respir Crit Care Med.  
>       *rs641525* is associated with *Emphysema-related traits.*  
>       **Annotation** emphysema [http://www.ebi.ac.uk/efo/EFO_0000464].  
>       **Parent(s)** lung disease.  
>       **Has disease location** lung.  

If you look closely, you'll see that "lung" is not mentioned anywhere in our data, only the extra fields that have come from the ontology.  We'd actually have picked this result up by including parents (`lung disease`), but this is only because EFO nicely defines hierarchy.  If we were using a different ontology with a different hierarchy (maybe one which doesn't use hierarchy in the ways we'd like), we can use a relationship other than `is a` to find this result.

Next, we tried searching for `schizophrenia`.  Let's try this again - yep, still 51 results.  You'll notice if we include parent terms, we still get 51 results - our order might shuffle around a bit though. 
This isn't unexpected - most of our data about schizophrenia should be nicely mapped to a specific term and would include the text "schizophrenia" in the title or the annotation line.
But last time we tried to search for other `mental disorder` and found no results at all.  Now, if we search including child and parent labels, we get more than 100 results! This covers a wide range of disorders, like "schizophrenia", "bipolar disorder" and many more.  For example:

> 1.    **Cross-disorder genomewide analysis of schizophrenia, bipolar disorder, and depression.**  
>       Huang J - Am J Psychiatry  
>       *rs1001021* is associated with *Schizophrenia, bipolar disorder and depression (combined)*  
>       **Annotation** bipolar disorder [http://www.ebi.ac.uk/efo/EFO_0000289]  
>       **Parent(s)** mental or behavioural disorder  

This shows the power of including additional information from the ontology in your Solr index. You'll also see the search is just as fast as it was previously: by including extra data when we built our index, we have almost no penalty in search time - which is usually the best option for users.

#### Additional Tasks

- [x] Play around with the index some more
- [x] Can you redo the searches for anatomical features from earlier?  What happens if you search by `heart` or `liver` and include child terms?
- [x] Try checking extra boxes to include additional relations.  Can you find more ways to search the data?

## Conclusions

This is the end of the BioSolr ontology expansion tutorial. You've seen how to install Solr, load some example data, extend Solr with the ontology expansion plugin developed by BioSolr into a Solr installation, and you've seen some of the extra features this plugin can give you.

If you have any comments, questions or feedback on this demo, you can use the tracker for this repository here - https://github.com/flaxsearch/BioSolr/issues, or send an email to matt@flax.co.uk or tburdett@ebi.ac.uk.

*BioSolr is funded by the BBSRC Flexible Interchange Programme (FLIP) grant number BB/M013146/1*


BioSolr
=======

Funded by the BBSRC http://www.bbsrc.ac.uk/ this collaboration between Flax and the European Bioinformatics Institute (http://www.ebi.ac.uk/) aims “to significantly advance the state of the art with regard to indexing and querying biomedical data with freely available open source software”. Here's some background:
http://www.flax.co.uk/blog/2014/06/11/biosolr-building-better-search-for-bioinformatics/

Here's a poster about the project http://f1000research.com/posters/4-491 and presentation http://f1000research.com/slides/4-492

We'll be using this repository to publish the open source software we develop to enhance and improve the use of the Apache Lucene/Solr search engine for this important sector.

If you're interested in joining this exciting collaboration please contact Flax via:
http://www.flax.co.uk/contact_us
and/or Dr Sameer Velankar via
http://www.ebi.ac.uk/about/people/sameer-velankar

To round off this phase of the BioSolr project there was an open workshop on 3rd/4th February 2016 at EMBL-EBI http://www.ebi.ac.uk/pdbe/about/events/open-source-search-bioinformatics. The papers presented are available in the 'workshop' folder. You can also read BioSolr-related blog posts at http://www.flax.co.uk/?s=biosolr&submit=Searchhttp://www.flax.co.uk/?s=biosolr&submit=Search
