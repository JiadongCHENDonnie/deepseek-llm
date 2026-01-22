#!/usr/bin/env python3
"""
Conversation Self-Review and Language Understanding Analyzer

This utility helps users analyze their conversations to:
1. Understand mixed language usage
2. Identify grammar patterns and short words
3. Provide self-review insights for improvement
"""

import re
from typing import Dict, List, Tuple
from collections import Counter


class ConversationAnalyzer:
    """
    Analyzes conversations for language mixing, grammar patterns, and provides
    self-review insights.
    """

    def __init__(self):
        """Initialize the conversation analyzer."""
        # Common short words that might indicate informal communication
        self.short_words = set(['i', 'u', 'r', 'y', 'k', 'ok', 'thx', 'pls'])
        
        # Language patterns (simplified detection)
        self.language_patterns = {
            'english': re.compile(r'[a-zA-Z]'),
            'chinese': re.compile(r'[\u4e00-\u9fff]'),
            'numbers': re.compile(r'\d'),
            'punctuation': re.compile(r'[^\w\s]')
        }

    def analyze_conversation(self, text: str) -> Dict:
        """
        Analyze a conversation text for language mixing, grammar, and patterns.

        Args:
            text: The conversation text to analyze

        Returns:
            Dictionary containing analysis results
        """
        if not text:
            return {
                'error': 'Empty text provided',
                'recommendations': ['Please provide text to analyze']
            }

        analysis = {
            'language_distribution': self._analyze_languages(text),
            'word_statistics': self._analyze_words(text),
            'grammar_insights': self._analyze_grammar(text),
            'mixed_language_usage': self._detect_language_mixing(text),
            'recommendations': []
        }

        # Generate recommendations based on analysis
        analysis['recommendations'] = self._generate_recommendations(analysis)

        return analysis

    def _analyze_languages(self, text: str) -> Dict[str, float]:
        """
        Detect and quantify language usage in the text.

        Args:
            text: Input text

        Returns:
            Dictionary with language distribution percentages
        """
        total_chars = len(text)
        if total_chars == 0:
            return {}

        lang_counts = {}
        for lang_name, pattern in self.language_patterns.items():
            matches = pattern.findall(text)
            lang_counts[lang_name] = (len(matches) / total_chars) * 100

        return lang_counts

    def _analyze_words(self, text: str) -> Dict:
        """
        Analyze word patterns including length and short word usage.

        Args:
            text: Input text

        Returns:
            Dictionary with word statistics
        """
        words = re.findall(r'\b\w+\b', text.lower())
        
        if not words:
            return {
                'total_words': 0,
                'unique_words': 0,
                'short_words_count': 0,
                'avg_word_length': 0
            }

        word_lengths = [len(word) for word in words]
        short_words_found = [word for word in words if word in self.short_words]

        return {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'short_words_count': len(short_words_found),
            'short_words_used': list(set(short_words_found)),
            'avg_word_length': sum(word_lengths) / len(words) if words else 0,
            'word_length_distribution': Counter(word_lengths)
        }

    def _analyze_grammar(self, text: str) -> Dict:
        """
        Analyze basic grammar patterns in the text.

        Args:
            text: Input text

        Returns:
            Dictionary with grammar insights
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        insights = {
            'sentence_count': len(sentences),
            'avg_sentence_length': 0,
            'capitalization_issues': 0,
            'missing_punctuation': 0
        }

        if sentences:
            total_words = sum(len(re.findall(r'\b\w+\b', s)) for s in sentences)
            insights['avg_sentence_length'] = total_words / len(sentences)

            # Check for capitalization issues
            for sentence in sentences:
                if sentence and not sentence[0].isupper():
                    insights['capitalization_issues'] += 1

        # Check for potential missing punctuation (sentences without end punctuation)
        if text and text[-1] not in '.!?':
            insights['missing_punctuation'] = 1

        return insights

    def _detect_language_mixing(self, text: str) -> Dict:
        """
        Detect patterns of language mixing within the text.

        Args:
            text: Input text

        Returns:
            Dictionary with language mixing insights
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        mixed_sentences = []
        for sentence in sentences:
            has_english = bool(self.language_patterns['english'].search(sentence))
            has_chinese = bool(self.language_patterns['chinese'].search(sentence))

            if has_english and has_chinese:
                mixed_sentences.append(sentence)

        return {
            'is_mixed_language': len(mixed_sentences) > 0,
            'mixed_sentence_count': len(mixed_sentences),
            'total_sentences': len(sentences),
            'mixing_percentage': (len(mixed_sentences) / len(sentences) * 100) 
                                if sentences else 0
        }

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """
        Generate self-review recommendations based on analysis.

        Args:
            analysis: Analysis results

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Check language mixing
        if analysis['mixed_language_usage']['is_mixed_language']:
            mix_pct = analysis['mixed_language_usage']['mixing_percentage']
            recommendations.append(
                f"Language Mixing Detected: {mix_pct:.1f}% of sentences mix languages. "
                "Consider using consistent language within sentences for clarity."
            )

        # Check short words usage
        word_stats = analysis['word_statistics']
        if word_stats.get('short_words_count', 0) > 0:
            recommendations.append(
                f"Informal Short Words: Found {word_stats['short_words_count']} "
                f"informal short words ({', '.join(word_stats.get('short_words_used', []))}). "
                "Consider using complete words for formal communication."
            )

        # Check grammar issues
        grammar = analysis['grammar_insights']
        if grammar.get('capitalization_issues', 0) > 0:
            recommendations.append(
                f"Capitalization: {grammar['capitalization_issues']} sentences lack "
                "proper capitalization. Start sentences with capital letters."
            )

        if grammar.get('missing_punctuation', 0) > 0:
            recommendations.append(
                "Punctuation: Missing end punctuation. "
                "Ensure sentences end with appropriate punctuation."
            )

        # Positive feedback
        if not recommendations:
            recommendations.append(
                "Good communication! Your text shows consistent language use "
                "and proper grammar patterns."
            )

        return recommendations

    def self_review_report(self, text: str) -> str:
        """
        Generate a comprehensive self-review report for the conversation.

        Args:
            text: Conversation text to analyze

        Returns:
            Formatted report string
        """
        analysis = self.analyze_conversation(text)

        if 'error' in analysis:
            return f"Error: {analysis['error']}"

        report_lines = [
            "=" * 60,
            "CONVERSATION SELF-REVIEW REPORT",
            "=" * 60,
            "",
            "Language Distribution:",
        ]

        # Language distribution
        for lang, percentage in analysis['language_distribution'].items():
            if percentage > 0:
                report_lines.append(f"  - {lang.capitalize()}: {percentage:.1f}%")

        # Word statistics
        report_lines.extend([
            "",
            "Word Statistics:",
            f"  - Total words: {analysis['word_statistics']['total_words']}",
            f"  - Unique words: {analysis['word_statistics']['unique_words']}",
            f"  - Average word length: {analysis['word_statistics']['avg_word_length']:.1f}",
        ])

        if analysis['word_statistics'].get('short_words_count', 0) > 0:
            report_lines.append(
                f"  - Short/informal words: {analysis['word_statistics']['short_words_count']}"
            )

        # Grammar insights
        report_lines.extend([
            "",
            "Grammar Insights:",
            f"  - Sentences: {analysis['grammar_insights']['sentence_count']}",
            f"  - Avg words per sentence: {analysis['grammar_insights']['avg_sentence_length']:.1f}",
        ])

        # Language mixing
        mixing = analysis['mixed_language_usage']
        report_lines.extend([
            "",
            "Language Mixing:",
            f"  - Mixed language usage: {'Yes' if mixing['is_mixed_language'] else 'No'}",
            f"  - Mixed sentences: {mixing['mixed_sentence_count']} / {mixing['total_sentences']}",
        ])

        # Recommendations
        report_lines.extend([
            "",
            "Recommendations for Improvement:",
        ])
        for i, rec in enumerate(analysis['recommendations'], 1):
            report_lines.append(f"  {i}. {rec}")

        report_lines.extend([
            "",
            "=" * 60,
        ])

        return "\n".join(report_lines)


def main():
    """Main function for command-line usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python conversation_analyzer.py <text>")
        print("\nExample:")
        print('  python conversation_analyzer.py "Hello world! This is a test."')
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    analyzer = ConversationAnalyzer()
    report = analyzer.self_review_report(text)
    print(report)


if __name__ == "__main__":
    main()
