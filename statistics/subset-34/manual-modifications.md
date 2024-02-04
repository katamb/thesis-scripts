# This document records all the manual changes made to the results to be more "fair"

Problems identified:
* RCI scripts sometimes just say the initial analysis was correct, but provide N/A for the vulnerability. In that case, the vulnerability field should be filled automatically. Can be fixed.
* Sometimes, the CWE-id is just given as a number. Manual fix should be acceptable for those, as changing the pattern could cause bigger issues.
* There is 2 more categories of results:
  * Files, where the given vulnerability is not present, but some other vulnerability is found (could be considered true negative?)
  * Files, where the given vulnerability is present, but some other vulnerability is found (could be considered false negative?)

Manual fixes done for llm-rci-results:
* For basic_prompt_rci_improve prompt and file J19500, the CWE-918 was manually added
* For basic_prompt_rci_improve prompt and file J19736, the CWE-476 was manually added
* For basic_prompt_rci_improve prompt and file J22026, the CWE-20 was manually added
* For basic_prompt_rci_improve prompt and file J22420, the CWE-79 was manually added
* 