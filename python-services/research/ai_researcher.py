"""AI-powered research using Tavily or Perplexity."""
from typing import Optional, List
from tenacity import retry, stop_after_attempt


class AIResearcher:
    """AI-powered research using Tavily or Perplexity."""

    def __init__(self, api_key: str, service: str = "tavily"):
        """
        Initialize AI research client.

        Args:
            api_key: API key for research service
            service: 'tavily' or 'perplexity'
        """
        self.service = service
        self.api_key = api_key
        if service == "tavily":
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=api_key)
            except ImportError:
                raise ImportError("Please install tavily-python: pip install tavily-python")

    @retry(stop=stop_after_attempt(3))
    async def research_project(
        self,
        project_url: str,
        project_name: str = None,
        deep_research: bool = True
    ) -> dict:
        """
        Conduct comprehensive research on a crypto project.

        Args:
            project_url: Project website URL
            project_name: Project name (if known)
            deep_research: Use deep research mode for comprehensive analysis

        Returns:
            dict: Structured research data
        """
        # Build comprehensive research query
        query = self._build_research_query(project_url, project_name)

        # Perform research
        if self.service == "tavily":
            result = await self._tavily_research(query, deep_research)
        else:
            result = await self._perplexity_research(query)

        return result

    def _build_research_query(self, project_url: str, project_name: str = None) -> str:
        """Build comprehensive research query."""
        base = f"Comprehensive analysis of {project_url}"
        if project_name:
            base = f"Comprehensive analysis of {project_name} crypto project {project_url}"

        base += " including: features, tokenomics, technology, team, roadmap, use cases"
        return base

    async def _tavily_research(self, query: str, deep_research: bool = False) -> dict:
        """Execute Tavily research."""
        search_depth = "advanced" if deep_research else "basic"

        response = self.client.search(
            query=query,
            search_depth=search_depth,
            max_results=10,
            include_answer=True,
            include_raw_content=False
        )

        return response

    async def _perplexity_research(self, query: str) -> dict:
        """Execute Perplexity research (alternative)."""
        # To be implemented when Perplexity API is available
        raise NotImplementedError("Perplexity research not yet implemented")
