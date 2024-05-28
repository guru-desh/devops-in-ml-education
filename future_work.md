# Future Work

Our current CI/CD pipeline has significantly streamlined the HW
development process. However, we can still focus on bringing future
improvements to enhance its efficiency. One key area of improvement is
the adoption of virtual machines with more compute power and various
operating systems to run the GitHub Actions, ensuring faster and more
reliable builds. We plan to explore tools like AWS EC2 [^1] to provision
high-performance VMs. In addition, telemetry will provide valuable
insights into resource utilization and performance bottlenecks, and
tools such as AWS CloudWatch [^2] to visualize telemetry data.

To ensure homework compatibility across various student environments, we
aim to expand the pipeline to test the Anaconda environments and Jupyter
Notebooks on different operating systems including macOS, Windows, and
varying architectures such as Apple Silicon. Setting up VMs for each
target platform will be crucial in achieving this goal.

We also plan to switch from our current testing framework, unittest, to
pytest . Pytest offers extended functionality such as its fixtures
feature which has great potential to enhance test readability and reuse.
Integrating code coverage analysis into the pipeline will allow us to
measure the effectiveness of the autograder tests in covering student
code. Tools like Codecov [^3] will be explored to generate code coverage
reports and identify areas for improvement in the autograder tests.

Lastly, we plan to also implement more formatting checks when a TA
commits code or opens a PR. Our current use of tools like black and nbqa
helps enforce coding standards, but we still face challenges in
verifying the consistency of Jupyter notebooks after changes. This is
primarily because the changes displayed on GitHub for Jupyter notebooks
show the raw JSON representation of the notebook rather than the
rendered notebook interface, making it difficult to review and
understand the changes in the context of the notebook’s structure and
layout. By introducing ReviewNB [^4] into the pipeline, we can smooth
out the process of examining outputs from Jupyter Notebooks by
pre-emptively monitoring the outputs before a merge.

By focusing on these areas, we aim to further streamline the HW
development process, reduce manual effort, and provide a more robust and
efficient CI/CD pipeline. Implementing these enhancements will not only
benefit our instructional team but also serve as a valuable resource for
other classes looking to adopt DevOps practices in their curriculum.

[^1]: https://aws.amazon.com/ec2/

[^2]: https://aws.amazon.com/cloudwatch/

[^3]: https://about.codecov.io/

[^4]: https://www.reviewnb.com/
