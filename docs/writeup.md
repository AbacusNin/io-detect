# io-detect: detecting coordinated inauthentic behavior

io-detect is a tested program that flags likely coordinated influence activity in social media data. It runs on data where the true answer is already known, so you can check its accuracy instead of taking my word for it. On a real set of Russian troll accounts it caught about two-thirds of them, and a little over half of what it flagged turned out to be real. The rest of this covers how it does that, and where it comes up short.

## The problem

An influence operation is a coordinated push, usually run by a state or a paid group, where many accounts pretend to be independent people all saying the same thing. The catch is that any single post looks normal. You cannot spot the operation by reading one account or checking one claim. What exposes it is coordination: several accounts resharing the same post within seconds of each other, the same sentence turning up word for word on accounts that supposedly have nothing to do with one another, or a hashtag that goes from quiet to flooded the moment dozens of unrelated accounts land on it together.

So io-detect does not try to decide whether an account is a bot or whether a claim is true. Those calls are usually impossible to make from the data. It measures coordination, which you can actually count.

## The data

This tool was measured on a public Indiana University dataset: roughly a million posts from a verified Russian campaign, released alongside ordinary accounts that were posting about the same topics in the same period. Those ordinary accounts are labeled as controls.

You need both sides to score a detector honestly. A tool that flags everything looks perfect right up until you check it against the accounts you know were innocent. The controls are what make that check possible.

The tool also reads a second dataset, the Clemson version of the same troll network, through the same loader, which is what forced the ingest layer to cope with more than one file format. The measured numbers below come only from the Indiana data, because that is the set that ships controls.

## How it works

The pipeline runs in stages:

- Normalize every dataset into one common record shape.
- Compute plain behavioral signals per account and per pair of accounts: resharing the same originals within a short window, posting identical text, flooding a hashtag, piling onto one target with mentions and replies.
- Build a network where two accounts are linked when they keep acting together, and the link gets heavier the more they do it.
- Find the dense knots in that network. Ordinary users spread out into a loose, sparse web, while a coordinated group clumps together into a tight cluster. The tool keeps only the clusters that are both large enough and tightly linked enough to stand apart from normal activity.
- Inside a flagged cluster, sort the members: the likely-automated accounts go one way, the ones that mostly amplify go the other.
- Tag each detected behavior with the matching DISARM technique (DISARM is an open catalog of influence-operation tactics), then score the flagged accounts against the dataset's known labels.

One design rule matters here: behavior gets detected first and named second. The DISARM tags are output only. They never feed back into the detection, so nothing gets flagged because of a label somebody stuck on it.

## Results

Scored at the account level on the Russian campaign data:

- Recall was about 0.67. Of the accounts genuinely in the operation, the tool caught roughly two-thirds.
- Precision was about 0.54. Of the accounts it flagged, a little over half were real and the rest were false alarms.

The exact counts sit in the repository. These are modest numbers. They are reported with the false alarms included instead of rounding them up, because that is genuinely what the test showed.

## What it does not do

- It does not work on live data. It was measured on old data with a known answer key. Live feeds have no answer key, and real operations are rare next to ordinary heated argument, so false alarms climb once you leave the lab. Read the numbers above as a best case.
- It does not attribute. Showing that a set of accounts acted together says nothing about which government or group paid for it. That is a separate judgment, and a human makes it.
- It does not police opinions. Real grassroots movements coordinate too. Telling a genuine movement apart from a paid operation is the hard part, and the tool leaves it to a reviewer.
- One of its signals did nothing on this data. The automation check reads the posting-app field, and Indiana replaced that field with anonymized codes, so it contributed zero. This writeup says so instead of papering over it.

## How it is built

Python, with polars for the data work and networkx for the graph. It was built test-first, 30 tests, all green. It ships under Apache 2.0 with a one-command demo that runs on a small built-in sample, so someone can watch it work without the large gated dataset. The datasets themselves are never bundled. The repo carries fetch instructions and checksums instead, which keeps it inside the datasets' licenses.

## Where it could go

A few directions are open. One is turning this into a running service. Another is adding a third dataset with a different shape, such as a platform takedown archive that splits accounts and posts into separate tables, which would stretch the ingest design further. The automation signal could also come back to life on data that keeps the posting-app field intact.
