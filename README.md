# README: Code for "Advances in AI Since 2020"

## Introduction

This repository contains the code used to analyze and generate the figures for the article, *"Advances in AI Since 2020: A Quantitative and Qualitative Overview."* The study examines the evolution of AI through both qualitative advancements (in natural language processing, deep learning, and scientific impact) and quantitative analysis (tracking AI-related publications in the OpenAlex database).

## Requirements

The code was developed in Python 3.12, using the following libraries:
- **pandas** 2.2.2
- **numpy** 1.26.4
- **scipy** 1.13.1
- **matplotlib** 3.9.2

Ensure these versions (or compatible ones) are installed in your environment.

## Data

We use the **OpenAlex** API as our primary data source, which contains metadata for over 209 million scholarly works. The code extracts metadata related to AI/ML papers, tracking the frequency of AI-related terminology and their applications across various scientific fields.

For more information about OpenAlex, visit [OpenAlex documentation](https://docs.openalex.org).
